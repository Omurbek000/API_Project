from django.db.models import F, Exists, OuterRef, Count
from django.shortcuts import get_list_or_404

from .models import Post, Comment, Favorite, Message, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class PostService:
    """
    Сервис для работы с постами.
    Здесь находится бизнес‑логика, которая НЕ должна быть во viewset.
    """

    @staticmethod
    def get_public_posts():
        """
        Возвращает опубликованные посты с оптимизацией.
        """
        return (
            Post.objects.published()
            .select_related("author", "category")
            .annotate(
                favorites_count=Count("favorited_by"),
                comments_count=Count("comments"),
            )
        )

    @staticmethod
    def get_post_for_detail(post_id, user):
        """
        Возвращает пост для детального просмотра.
        Добавляет:
        - favorites_count
        - is_favorited
        """
        return (
            Post.objects
            .select_related("author", "category")
            .annotate(
                favorites_count=Count("favorited_by"),
                is_favorited=Exists(
                    Favorite.objects.filter(user=user, post_id=OuterRef("pk"))
                ),
            )
            .get(pk=post_id)
        )

    @staticmethod
    def increase_views(post: Post):
        """
        Увеличивает просмотры безопасно (без гонок).
        """
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)


class CommentService:
    """
    Сервис для комментариев.
    """

    @staticmethod
    def get_root_comments(post_id):
        """
        Возвращает только корневые комментарии (parent=None).
        """
        return (
            Comment.objects
            .filter(post_id=post_id, parent=None)
            .select_related("author")
            .prefetch_related("replies")
        )

    @staticmethod
    def create_comment(user, post_id, text, parent=None):
        """
        Создаёт комментарий.
        """
        return Comment.objects.create(
            author=user,
            post_id=post_id,
            text=text,
            parent=parent
        )


class FavoriteService:
    """
    Сервис для избранного.
    """

    @staticmethod
    def add_to_favorites(user, post_id):
        """
        Добавляет пост в избранное.
        """
        return Favorite.objects.create(user=user, post_id=post_id)

    @staticmethod
    def remove_from_favorites(user, post_id):
        """
        Удаляет пост из избранного.
        """
        fav = get_object_or_404(Favorite, user=user, post_id=post_id)
        fav.delete()

    @staticmethod
    def toggle_favorite(user, post_id):
        """
        Переключает избранное:
        - если есть → удалить
        - если нет → добавить
        """
        fav = Favorite.objects.filter(user=user, post_id=post_id).first()
        if fav:
            fav.delete()
            return False
        Favorite.objects.create(user=user, post_id=post_id)
        return True


class MessageService:
    """
    Сервис для личных сообщений.
    """

    @staticmethod
    def send_message(sender, recipient_id, text):
        """
        Отправляет сообщение.
        """
        return Message.objects.create(
            sender=sender,
            recipient_id=recipient_id,
            text=text
        )

    @staticmethod
    def get_dialog(user, other_user_id):
        """
        Возвращает переписку между двумя пользователями.
        """
        return (
            Message.objects
            .filter(
                (F("sender") == user and F("recipient_id") == other_user_id) |
                (F("sender_id") == other_user_id and F("recipient") == user)
            )
            .order_by("created_at")
        )

    @staticmethod
    def mark_as_read(message_id, user):
        """
        Помечает сообщение как прочитанное.
        """
        msg = get_object_or_404(Message, pk=message_id, recipient=user)
        msg.is_read = True
        msg.save()
        return msg

    @staticmethod
    def unread_count(user):
        """
        Количество непрочитанных сообщений.
        """
        return Message.objects.filter(recipient=user, is_read=False).count()


# Что мы сделали в SERVICES?
# ✔ Вынесли бизнес‑логику из viewset'ов
# Теперь viewset — только контроллер, а не мешанина логики.

# ✔ Добавили toggle_favorite
# Теперь избранное работает как на YouTube.

# ✔ Добавили unread_count
# Теперь можно показывать индикатор непрочитанных сообщений.

# ✔ Добавили оптимизированные запросы
# select_related, prefetch_related, Exists, Count.

# ✔ Добавили PostService.get_post_for_detail
# Теперь детальная страница поста работает без N+1.