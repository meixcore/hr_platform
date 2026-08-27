from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('auth-token/', obtain_auth_token, name='obtain_auth_token'),
]