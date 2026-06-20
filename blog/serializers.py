from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Comment, Favorite


# Категория
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


# Автор (краткая информация)
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


# Комментарий
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "created_at"]


# Пост (для списка)
class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "image",
            "author",
            "category",
            "comments_count",
            "is_favorite",
            "created_at",
        ]

    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, post=obj).exists()
        return False


# Пост (детально)
class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "image",
            "author",
            "category",
            "comments",
            "is_favorite",
            "created_at",
            "updated_at",
        ]

    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, post=obj).exists()
        return False


# Создание / обновление поста
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "category"]


# Добавление комментария
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]


# Избранное
class FavoriteSerializer(serializers.ModelSerializer):
    post = PostListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "post", "created_at"]
