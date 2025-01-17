# urls.py
from django.urls import path
from .views import VideoUploadView, VideoSearchView, CategoryListView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('search/', VideoSearchView.as_view(), name='video-search'),
    path('category/<int:category_id>/', CategoryListView.as_view(), name='category-videos'),

]
