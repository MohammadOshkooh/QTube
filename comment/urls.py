from django.urls import path
from .views import CommentListView, CommentCreateView

urlpatterns = [
    path('videos/comments/', CommentListView.as_view(), name='comment-list'),
    path('videos/comments/create/', CommentCreateView.as_view(), name='comment-create'),
]
