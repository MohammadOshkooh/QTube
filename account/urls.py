from django.urls import path
from .views import UserRegistrationView, UserLoginView, UsersForgotPasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('password-reset/', UsersForgotPasswordView.as_view(), name='password-reset'),
]
