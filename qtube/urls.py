# urls.py
from django.urls import path
from .views import VideoUploadView, VideoSearchView, CategoryListView, GetVideoByCategoryListView, UserUploadedVideosView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('my-videos/', UserUploadedVideosView.as_view(), name='my-videos'),
    path('search/', VideoSearchView.as_view(

    ), name='video-search'),
    path('category/<int:category_id>/', GetVideoByCategoryListView.as_view(), name='video-by-category-videos'),
    path('categories/', CategoryListView.as_view(), name='category-videos'),

]
