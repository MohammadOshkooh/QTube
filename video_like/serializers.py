class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'video', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']