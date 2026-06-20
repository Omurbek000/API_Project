from django.urls import path
from .views import (
    DialogListView,
    DialogCreateView,
    MessageListView,
    MessageCreateView
)

urlpatterns = [
    # Диалоги
    path("dialogs/", DialogListView.as_view(), name="dialogs-list"),
    path("dialogs/create/<int:user_id>/", DialogCreateView.as_view(), name="dialog-create"),

    # Сообщения
    path("dialogs/<int:dialog_id>/messages/", MessageListView.as_view(), name="messages-list"),
    path("dialogs/<int:dialog_id>/messages/send/", MessageCreateView.as_view(), name="message-send"),
]
