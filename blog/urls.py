from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.category import CategoryViewSet
from .views.post import PostViewSet
from .views.comment import CommentViewSet

router = DefaultRouter()

# Категории (только чтение)
router.register("categories", CategoryViewSet, basename="category")

# Посты (CRUD + actions)
router.register("posts", PostViewSet, basename="post")

# Вложенные комментарии:
# /api/posts/<slug>/comments/
router.register(
    r"posts/(?P<post_slug>[^/.]+)/comments",
    CommentViewSet,
    basename="post-comments"
)

urlpatterns = [
    path("", include(router.urls)),
]
