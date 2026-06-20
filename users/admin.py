from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "colored_status", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)
    inlines = (ProfileInline,)

    def colored_status(self, obj):
        color = "green" if obj.is_active else "red"
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            "ACTIVE" if obj.is_active else "DISABLED"
        )

    colored_status.short_description = "Status"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
