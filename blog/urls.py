from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    PostViewSet,
    CommentViewSet,
    FavoriteToggleView,
    FavoriteListView
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    # Основные маршруты (categories, posts)
    path("", include(router.urls)),

    # Комментарии (вложенные)
    path("posts/<int:post_id>/comments/", 
         CommentViewSet.as_view({"get": "list", "post": "create"}), 
         name="comments-list-create"),

    path("posts/<int:post_id>/comments/<int:pk>/",
         CommentViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
         name="comments-detail"),

    # Избранное
    path("posts/<int:post_id>/favorite/", FavoriteToggleView.as_view(), name="favorite-toggle"),
    path("favorites/", FavoriteListView.as_view(), name="favorites-list"),
]
