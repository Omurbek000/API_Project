from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    ProfileView,
    ProfileUpdateView,
    LogoutView
)

urlpatterns = [
    # Регистрация (с выдачей JWT)
    path("register/", RegisterView.as_view(), name="register"),

    # JWT авторизация
    path("login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Logout (через blacklist)
    path("logout/", LogoutView.as_view(), name="jwt-logout"),

    # Профиль
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
]
