# jwtauth/urls.py

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import registration, login

app_name = "auth"

urlpatterns = [
    path("register", registration, name="register"),
    path("login", login, name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
