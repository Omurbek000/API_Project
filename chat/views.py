from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Dialog, Message
from .serializers import (
    DialogSerializer,
    MessageSerializer,
    MessageCreateSerializer
)


# Получить список диалогов пользователя
class DialogListView(generics.ListAPIView):
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Dialog.objects.filter(user1=user) | Dialog.objects.filter(user2=user)


# Создать диалог или вернуть существующий
class DialogCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user1 = request.user
        user2 = get_object_or_404(User, id=user_id)

        if user1 == user2:
            return Response({"error": "Нельзя создать диалог с самим собой"}, status=400)

        dialog, created = Dialog.objects.get_or_create(
            user1=min(user1, user2, key=lambda u: u.id),
            user2=max(user1, user2, key=lambda u: u.id)
        )

        return Response(DialogSerializer(dialog, context={"request": request}).data)


# Получить сообщения диалога
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dialog = get_object_or_404(Dialog, id=self.kwargs["dialog_id"])
        user = self.request.user

        if user not in [dialog.user1, dialog.user2]:
            return Message.objects.none()

        # Отмечаем входящие сообщения как прочитанные
        dialog.messages.filter(is_read=False).exclude(sender=user).update(is_read=True)

        return dialog.messages.all().order_by("created_at")


# Отправить сообщение
class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dialog_id):
        dialog = get_object_or_404(Dialog, id=dialog_id)
        user = request.user

        if user not in [dialog.user1, dialog.user2]:
            return Response({"error": "Нет доступа к диалогу"}, status=403)

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            dialog=dialog,
            sender=user,
            text=serializer.validated_data["text"]
        )

        return Response(MessageSerializer(message).data, status=201)
