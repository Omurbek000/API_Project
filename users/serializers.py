from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


# Профиль пользователя
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["avatar", "bio", "created_at", "updated_at"]


# Информация о пользователе
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


# Регистрация
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user


# Логин
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль")
        data["user"] = user
        return data
