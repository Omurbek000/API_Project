from django.contrib import admin
from .models import Category, Post, Comment, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "created_at", "updated_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "author__username")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")
    search_fields = ("author__username", "post__title")
    ordering = ("-created_at",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    ordering = ("-created_at",)
