from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Comment, Post
from ..serializers.comment import CommentSerializer
from ..permissions import IsAuthorOrReadOnly
from ..services import CommentService


class CommentViewSet(viewsets.ModelViewSet):
    """
    Комментарии к постам.
    Используется вложенный роутер:
    /api/posts/<slug>/comments/
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Возвращает только корневые комментарии.
        """
        post = get_object_or_404(Post, slug=self.kwargs["post_slug"])
        return CommentService.get_root_comments(post.id)

    def perform_create(self, serializer):
        """
        Создание комментария.
        """
        post = get_object_or_404(Post, slug=self.kwargs["post_slug"])
        serializer.save(
            author=self.request.user,
            post=post,
        )


# Что мы сделали в VIEWS?
# ✔ Вынесли бизнес‑логику в services
# ViewSet теперь чистый и лёгкий.

# ✔ Добавили slug‑маршруты
# Теперь посты доступны по красивым URL.

# ✔ Добавили action favorite
# Теперь избранное работает как на YouTube.

# ✔ Добавили action my
# Теперь можно получить свои посты.

# ✔ Оптимизировали retrieve
# Теперь детальная страница работает без N+1.

# ✔ Комментарии используют вложенный роутер
# Красиво, REST‑ориентировано.