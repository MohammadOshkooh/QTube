from datetime import datetime

import phonenumbers
import pytz
from cities_light.models import Country
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from Authentication.auxiliary_functions import get_dict_from_redis, delete_item_from_redis
from Authentication.models import Schedule, User
from Level.models import EnglishLevel, User_English_Level


class UserBaseSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='phone_number', required=True, allow_null=False, allow_blank=True)
    active_time_zone = serializers.CharField(required=True, allow_null=False, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = ('phone', 'active_time_zone')

    def get_formal_phone_number(self, phone, nationality):
        national_code = nationality.code2
        parse_number = phonenumbers.parse(phone, national_code)
        if not phonenumbers.is_valid_number_for_region(parse_number, national_code):
            # phone number is not valid
            return None
        phone_with_code = phonenumbers.format_number(parse_number, phonenumbers.PhoneNumberFormat.E164)
        return phone_with_code[len(national_code) + 1:]

    def validate(self, data):
        active_time_zone = pytz.timezone(data.get('active_time_zone'))
        phone = data.get('phone_number')
        nationality = data.get('nationality')

        national = Country.objects.filter(name=active_time_zone).first()
        if not national:
            raise serializers.ValidationError(
                {'message': "Nationality doesn't exist, please enter nationality again!"})
        if active_time_zone == "":
            raise serializers.ValidationError({'message': "Active time zone is required!"})
        if phone == "":
            raise serializers.ValidationError({'message': "Phone number is required!"})
        formal_phone_number = self.get_formal_phone_number(phone, national)

        if not formal_phone_number:
            raise serializers.ValidationError({'message': "Please enter a valid phone number!"})

        data['phone_number'] = formal_phone_number
        data['active_time_zone'] = active_time_zone
        data['nationality'] = national
        return data


class UserCheckSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = UserBaseSerializer.Meta.fields

    def validate(self, data):
        data = super().validate(data)
        formal_phone_number = data['phone_number']
        user = get_user_model().objects.filter(phone_number=formal_phone_number).first()

        if user is None:
            raise serializers.ValidationError({'message': "User doesn't exist!"})

        data['user'] = user
        return data


class UserRegistrationSerializer(UserBaseSerializer):
    introducer_code = serializers.CharField(source='introducer', required=False, allow_null=True, allow_blank=True)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    gender = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    mac_address = serializers.CharField(required=False, allow_null=False, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = UserBaseSerializer.Meta.fields + ('username', 'password', 'gender', 'introducer_code', 'mac_address')

    def validate(self, data):
        data = super().validate(data)
        formal_phone_number = data.get('phone_number')

        if data.get('gender') == "":
            raise serializers.ValidationError({'message': "Gender is required!"})

        if data.get('username') == "":
            raise serializers.ValidationError({'message': "Username is required!"})

        if data.get('password') == "":
            raise serializers.ValidationError({'message': "Password is required!"})

        if data.get('mac_address') == "":
            raise serializers.ValidationError({'message': "MAC address is required!"})

        if User.objects.filter(phone_number=formal_phone_number).exists():
            raise serializers.ValidationError({'message': "This phone number exists! Please enter a new one"})

        introducer_code = data.get('introducer', None)
        if introducer_code and not User.objects.filter(ref_code=introducer_code).exists():
            raise serializers.ValidationError({'message': "introducer code is wrong"})

        current_time_in_zone = datetime.now(data['active_time_zone'])
        data['ref_code'] = str(hash(str(current_time_in_zone.timestamp())))[1:11]
        return data


class UserLoginSerializer(UserCheckSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, allow_null=False, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = UserCheckSerializer.Meta.fields + ('password',)

    def validate(self, data):
        data = super().validate(data)
        user = data['user']

        if data.get('password') == "":
            raise serializers.ValidationError({'message': "Password is required!"})

        if not user.check_password(data.get('password')):
            raise serializers.ValidationError({'message': "Incorrect password"})

        data['user'] = user
        return data


class UserChangePasswordSerializer(UserCheckSerializer):
    token = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, allow_null=True, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = UserBaseSerializer.Meta.fields + ('token', 'new_password')

    def check_token_status(self, phone, token):
        """
        0: Token expired
        1: Token is not valid
        2: Token is valid
        """
        # --- get redis data
        redis_data = get_dict_from_redis(f"{phone}_forgot_pass")
        if redis_data['status']:
            data = redis_data['data']

            # --- check token
            redis_token = int(data['token'])
            if redis_token != int(token):
                return 1
            return 2
        return 0

    def validate(self, data):
        data = super().validate(data)
        token = data.get('token')
        if token == "":
            raise serializers.ValidationError({'message': "Token is required!"})

        if not str(token).isnumeric():
            raise serializers.ValidationError({'message': "Please enter a valid token!"})

        phone = data.get('phone_number')

        print(self.check_token_status(phone, token))

        if self.check_token_status(phone, token) == 2:
            user = data['user']
            new_password = data.get('new_password')
            if new_password is None:
                raise serializers.ValidationError({'message': "New password is required!"})
            user.set_password(new_password)
            user.save()

            # --- Delete this record from redis
            delete_item_from_redis(f"{phone}_forgot_pass")
        else:
            raise serializers.ValidationError({'message': "Token is not correct!"})

        return data


class UserRestPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, allow_null=False, allow_blank=True)
    old_password = serializers.CharField(style={'input_type': 'password'}, allow_null=False, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = UserBaseSerializer.Meta.fields + ('new_password', 'old_password')

    def validate(self, data):
        data = super().validate(data)

        if data.get('old_password') == "":
            raise serializers.ValidationError({'message': "Old password is required!"})

        if data.get('new_password') == "":
            raise serializers.ValidationError({'message': "New password is required!"})


class UserSerializer(serializers.ModelSerializer):
    AI_Assistance = (
        ("SLT", "Alpha"),
        ("CLB", "Sara"),
        ("BDL", "Dav"),
        ("RMS", "Mo"),
        ("KSP", "Sali")
    )

    ai_assist_ai_name = serializers.SerializerMethodField()
    user_level = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", 'username', 'first_name', 'last_name', 'email', 'date_joined', 'phone_number', 'gender',
                  'active_time_zone', 'ai_assist_ai_name', 'nationality', 'ref_code', 'user_level', "is_prime",
                  'schedule')

    def get_schedule(self, obj):
        res = {}
        items = Schedule.objects.all().values()
        res["items"] = items
        if obj.schedule is None:
            res["selected_id"] = None
        else:
            res["selected_id"] = obj.schedule.id
        return res

    def get_ai_assist_ai_name(self, obj):
        if obj.ai_assist is None or obj.ai_assist == "":
            return None
        ai_assist_code = obj.ai_assist.ai_name
        ai_assist_name = dict(self.AI_Assistance).get(ai_assist_code)
        return ai_assist_name

    def get_user_level(self, obj):
        try:
            le = EnglishLevel.objects.get(user=obj).level
            level = dict(User_English_Level).get(le)
            return level
        except:
            return None


class PlanSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    remaining_time = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.amount_plan.title

    def get_created(self, obj):
        return obj.created.strftime("%Y-%m-%d")

    def get_end(self, obj):
        end_date = obj.created + timezone.timedelta(days=obj.amount_plan.expired)

        return end_date.strftime("%Y-%m-%d")

    def get_remaining_time(self, obj):
        diff = obj.created + timezone.timedelta(days=obj.amount_plan.expired) - timezone.now()
        days_difference = diff.days
        return int(days_difference) + 1