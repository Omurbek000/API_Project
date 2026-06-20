from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from ..models import Post
from ..serializers.post import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
)
from ..permissions import IsAuthorOrReadOnly
from ..services import PostService, FavoriteService


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet постов:
    - список опубликованных
    - создание
    - редактирование
    - удаление
    - детальный просмотр
    - мои посты
    - избранное (toggle)
    """

    lookup_field = "slug"  # Теперь посты доступны по slug

    def get_queryset(self):
        """
        Разные queryset для разных действий.
        """
        user = self.request.user

        # Мои посты (включая черновики)
        if self.action == "my":
            return (
                Post.objects.by_author(user)
                .select_related("author", "category")
                .annotate(
                    favorites_count=Count("favorited_by"),
                    comments_count=Count("comments"),
                )
            )

        # Детальный просмотр
        if self.action == "retrieve":
            return Post.objects.select_related("author", "category")

        # Список опубликованных
        return PostService.get_public_posts()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PostCreateUpdateSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [IsAuthorOrReadOnly()]

    def retrieve(self, request, *args, **kwargs):
        """
        Детальный просмотр поста + увеличение просмотров.
        """
        slug = kwargs["slug"]
        post = get_object_or_404(Post, slug=slug)

        # Увеличиваем просмотры
        PostService.increase_views(post)

        # Получаем оптимизированный объект
        post = PostService.get_post_for_detail(post.id, request.user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        """
        GET /api/posts/my/ — мои посты.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, slug=None):
        """
        POST /api/posts/<slug>/favorite/ — переключить избранное.
        """
        post = get_object_or_404(Post, slug=slug)
        is_fav = FavoriteService.toggle_favorite(request.user, post.id)
        return Response({"is_favorited": is_fav})
