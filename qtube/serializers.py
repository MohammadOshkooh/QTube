# serializers.py
from rest_framework import serializers
from .models import Video, Category


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'thumbnail',
            'category', 'views', 'processing_status', 'created_at', 'file'
        ]
        read_only_fields = ['views', 'processing_status', 'created_at']

    def validate_file(self, value):
        allowed_formats = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'mpeg', '3gp', 'ogg']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise serializers.ValidationError(
                "Unsupported file format. Supported formats: " + ", ".join(allowed_formats)
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
