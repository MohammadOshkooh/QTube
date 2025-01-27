
from django.urls import path

from video_like.views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path('videos/<int:video_id>/likes/', LikeListView.as_view(), name='like-list'),
    path('videos/<int:video_id>/likes/add/', LikeCreateView.as_view(), name='like-create'),
    path('videos/<int:video_id>/likes/remove/', LikeDeleteView.as_view(), name='like-delete'),
]
