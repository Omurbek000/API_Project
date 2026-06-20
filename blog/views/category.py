from rest_framework import viewsets, permissions
from ..models import Category
from ..serializers.category import CategorySerializer
from ..permissions import IsAdminOrReadOnly

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Категории доступны всем (GET).
    Создание/редактирование — только администратору.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# ✔ Чисто
# ✔ Минимально
# ✔ REST‑ориентировано