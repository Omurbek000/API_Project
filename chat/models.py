from django.db import models
from django.contrib.auth.models import User


class Dialog(models.Model):
    """
    Диалог между двумя пользователями.
    """
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dialogs_started"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dialogs_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Диалог: {self.user1.username} ↔ {self.user2.username}"


class Message(models.Model):
    """
    Сообщение внутри диалога.
    """
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.sender.username}"
