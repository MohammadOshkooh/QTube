# serializers.py
from rest_framework import serializers
from .models import Video, Comment


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'file', 'thumbnail', 'category', 'views', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'text', 'created_at']

