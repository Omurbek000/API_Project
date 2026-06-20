from django.contrib import admin
from django.utils.html import format_html
from .models import Dialog, Message


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ("id", "user1", "user2", "created_at")
    search_fields = ("user1__username", "user2__username")
    ordering = ("-created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "dialog", "sender", "colored_status", "created_at")
    search_fields = ("sender__username", "dialog__id")
    list_filter = ("is_read",)
    ordering = ("-created_at",)

    def colored_status(self, obj):
        color = "green" if obj.is_read else "red"
        text = "READ" if obj.is_read else "UNREAD"
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            text
        )

    colored_status.short_description = "Status"
