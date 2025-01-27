from django.urls import path
from .views import CommentListView, CommentCreateView

urlpatterns = [
    path('', CommentListView.as_view(), name='comment-list'),
    path('create/', CommentCreateView.as_view(), name='comment-create'),
]
