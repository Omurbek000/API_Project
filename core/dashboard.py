from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class CustomAdminSite(admin.AdminSite):
    site_header = "Aziat Admin Panel"
    site_title = "Aziat Admin"
    index_title = "Добро пожаловать"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["cards"] = [
            {
                "title": "Пользователи",
                "url": reverse("admin:auth_user_changelist"),
                "color": "#007bff",
            },
            {
                "title": "Посты",
                "url": reverse("admin:blog_post_changelist"),
                "color": "#28a745",
            },
            {
                "title": "Диалоги",
                "url": reverse("admin:chat_dialog_changelist"),
                "color": "#ffc107",
            },
        ]
        return super().index(request, extra_context)
