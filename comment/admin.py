from django.contrib import admin

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'text', 'created_at')
    list_filter = ('created_at', 'video')
    search_fields = ('text', 'user__username', 'video__title')
