from django.contrib import admin

from video_like.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ('user', 'video', 'like')