from rest_framework import serializers
from ..models import Comment
from .post import UserShortSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Комментарий с вложенными ответами.
    Ограничена глубина рекурсии (до 3 уровней).
    """

    author = UserShortSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','author','parent','text','is_deleted','created_at','replies']
        read_only_fields = ['id', 'author','created_at','is_deleted']

    def get_replies(self, obj):
        """
        Возвращает вложенные ответы.
        Ограничение глубины: максимум 3 уровня.
        """
        depth = self.context.get('depth',1)
        if depth >= 3:
            return []
        serializer = CommentSerializer(
            obj.replies.all()
            many=True,
            context={'depth': depth + 1 }
        )
        return serializer.data

    def validate_parent(self, value):
         """
        Проверка: parent должен относиться к тому же посту.
        """
         if value and value.post_id != self.context['post_id']:
            raise serializers.ValidationError("Ответ должен быть к комментарию этого же поста.")
         return value 

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        validated_data["post_id"] = self.context["post_id"]
        return super().create(validated_data)




#  Что мы сделали в SERIALIZERS?
# ✔ Разделили сериализаторы по модулям
# Теперь код чистый и легко поддерживаемый.

# ✔ Добавили excerpt
# Чтобы не тянуть весь текст в списке постов.

# ✔ Добавили slug
# Для SEO и красивых URL.

# ✔ Добавили is_favorited через аннотацию
# Больше нет лишних SQL‑запросов.

# ✔ Ограничили глубину комментариев
# Чтобы не было бесконечной рекурсии.

# ✔ Добавили favorites_count и comments_count через аннотации
# Быстро, эффективно, без N+1.