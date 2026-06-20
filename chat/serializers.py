from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dialog, Message


# Краткая информация о пользователе
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


# Сообщение
class MessageSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "is_read", "created_at"]


# Создание сообщения
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["text"]


# Диалог
class DialogSerializer(serializers.ModelSerializer):
    user1 = UserShortSerializer(read_only=True)
    user2 = UserShortSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = [
            "id",
            "user1",
            "user2",
            "created_at",
            "last_message",
            "unread_count",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        user = self.context["request"].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()
