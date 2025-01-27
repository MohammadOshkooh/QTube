from django.contrib import admin
from .models import Category, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'views', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('views',)


