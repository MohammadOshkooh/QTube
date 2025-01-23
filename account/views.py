from .serializers import LoginSerializer, RegisterSerializer, PasswordResetConfirmSerializer, \
    PasswordResetRequestSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from .utils import generate_random_token, add_dict_to_redis, send_token, get_dict_from_redis, delete_item_from_redis


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
            # new_user.set_password(serializer.data['password'])
            new_user.save()

            refresh = RefreshToken.for_user(new_user)
            refresh_code = str(refresh)
            access_code = str(refresh.access_token)

            return Response(
                {'message': "Congratulations, your account has been successfully created.", "access": access_code,
                 "refresh": refresh_code, "is_valid": True}, status=status.HTTP_200_OK)

        else:

            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            refresh = RefreshToken.for_user(user)
            refresh_code = str(refresh)
            access_code = str(refresh.access_token)

            return Response(
                {'message': "Login successful.", "access": access_code, "refresh": refresh_code, "is_valid": True},
                status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UsersForgotPasswordView(APIView):
    def post(self, request):

        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = serializer.validated_data.get('user')

            # --- generate token
            token = int(generate_random_token())
            redis_data = {
                "token": token,
                "user_id": user.id
            }
            # Todo
            if add_dict_to_redis(f"{email}_forgot_pass", redis_data, ex=1000):
                send_token(email, token=str(token))
                return Response({'message': 'Token successfully sent!', "Token": token, "expire_time": 120},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': "Please try again!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # --- check otp and set password
    def patch(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                token = request.data['token']
                new_password = request.data.get('new_password', None)
            except Exception as e:
                return Response({'message': f"request body is incorrect, {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            if not token:
                return Response({'message': "Please enter token!"}, status=status.HTTP_400_BAD_REQUEST)

            # --- check token type
            elif not str(token).isnumeric():
                return Response({'message': "Please enter a valid token!"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # --- get redis data
                redis_data = get_dict_from_redis(f"{email}_forgot_pass")
                if redis_data['status']:
                    data = redis_data['data']
                    # --- check token
                    redis_token = int(data['token'])
                    if redis_token != int(token):
                        return Response({'message': "Token isn't correct!"}, status=status.HTTP_400_BAD_REQUEST)
                    # --- get user
                    if not new_password:
                        return Response({"message": "Token is correct"})

                    user_id = data['user_id']
                    user = User.objects.get(id=user_id)
                    user.set_password(new_password)
                    user.save()
                    # --- Delete this record from redis
                    delete_item_from_redis(f"{email}_forgot_pass")
                    # --- response
                    return Response({'message': "Password successfully changed!"}, status=status.HTTP_200_OK)
                # --- something went wrong
                return Response({'message': "Token invalid or expired, try again!"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
