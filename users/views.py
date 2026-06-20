from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileSerializer
)


# Регистрация + автоматическая выдача JWT
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)


# Получение профиля
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Обновление профиля
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# Logout (JWT)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вы вышли из аккаунта"})
        except Exception:
            return Response({"error": "Неверный refresh токен"}, status=400)
