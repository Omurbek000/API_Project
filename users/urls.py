from django.urls import path
from .views.auth import RegisterView, LoginView, LogoutView, ChangePasswordView
from .views.profile import MeView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Авторизация
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),

    # Профиль
    path("me/", MeView.as_view(), name="me"),
    path("<int:pk>/", UserProfileView.as_view(), name="user_profile"),
]
