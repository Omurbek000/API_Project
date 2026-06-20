from rest_framework import serializers
from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model

from ..models import Post, Favorite, Category
from .category import CategorySerializer

User = get_user_model()

# ───────────────────────────── USER SHORT ─────────────────────────────


class UserShortSerializer(serializers.ModelSerializer):
    """
    Краткая информация об авторе.
    Используется в списках постов и комментариях.
    """

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


# ───────────────────────────── POST LIST ─────────────────────────────


class PostListSerializer(serializers.ModelSerializer):
    """
    Список постов.
    Лёгкий сериализатор для вывода карточек постов.
    """

    author = UserShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "image",
            "author",
            "category",
            "status",
            "views",
            "favorites_count",
            "comments_count",
            "created_at",
        ]


# ───────────────────────────── POST DETAIL ─────────────────────────────

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Детальная информация о посте.
    Добавлено поле is_favorited — отмечен ли пост пользователем.
    """

    author = UserShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    favorites_count = serializers.IntegerField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id", "title", "slug", "text", "excerpt", "image",
            "author", "category",
            "status", "views",
            "favorites_count", "is_favorited",
            "created_at", "updated_at",
        )




# ───────────────────────────── POST CREATE/UPDATE ─────────────────────────────
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Создание и редактирование поста.
    Автор автоматически подставляется из request.user.
    """

    class Meta:
        model = Post
        fields = ["title", "text", "image", "category", "status"]

    def create(self, validated_data):
        validated_data["author"] = self.context["reguest"].user
        return super().create(validated_data)
