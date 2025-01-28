
from django.urls import path

from video_like.views import LikeCreateView, LikeDeleteView, LikeListView

urlpatterns = [
    path('', LikeListView.as_view(), name='like-list'),
    path('add/', LikeCreateView.as_view(), name='like-create'),
    path('remove/', LikeDeleteView.as_view(), name='like-delete'),
]
