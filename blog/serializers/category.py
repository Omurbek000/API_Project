from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    Используется в списках, деталях и вложениях в постах.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
