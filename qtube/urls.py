# urls.py
from django.urls import path
from .views import VideoUploadView, VideoSearchView, CategoryListView, GetVideoByCategoryAPIView, \
    UserUploadedVideosView, CreateCategory

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('my-videos/', UserUploadedVideosView.as_view(), name='my-videos'),
    path('search/', VideoSearchView.as_view(

    ), name='video-search'),
    path('videos/', GetVideoByCategoryAPIView.as_view(), name='video-by-category-videos'),
    path('categories/', CategoryListView.as_view(), name='category-videos'),
    path('categories/create/', CreateCategory.as_view(), name='create-category'),

]
