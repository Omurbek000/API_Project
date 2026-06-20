from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Post, Comment, Favorite
from .serializers import (
    CategorySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    FavoriteSerializer
)
from .permissions import IsAuthorOrReadOnly
from .services import toggle_favorite
from django.shortcuts import get_object_or_404


# Категории
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Посты
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author", "category")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return PostListSerializer
        if self.action in ["retrieve"]:
            return PostDetailSerializer
        return PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Комментарии
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"]).select_related("author")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)


# Избранное (добавить / убрать)
class FavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        result = toggle_favorite(user=request.user, post_id=post_id)
        return Response(result, status=status.HTTP_200_OK)


# Список избранного
class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related("post")
        serializer = FavoriteSerializer(favorites, many=True, context={"request": request})
        return Response(serializer.data)
