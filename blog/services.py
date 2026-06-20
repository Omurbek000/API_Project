from django.shortcuts import get_object_or_404
from .models import Post, Favorite, Comment


# Добавить / убрать из избранного
def toggle_favorite(user, post_id):
    post = get_object_or_404(Post, id=post_id)

    favorite, created = Favorite.objects.get_or_create(
        user=user,
        post=post
    )

    if not created:
        favorite.delete()
        return {"status": "removed", "message": "Удалено из избранного"}

    return {"status": "added", "message": "Добавлено в избранное"}


# Создание комментария (если нужно использовать отдельно)
def create_comment(user, post_id, text):
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        author=user,
        post=post,
        text=text
    )
    return comment


# Получение списка комментариев (пример расширяемой логики)
def get_post_comments(post_id):
    return Comment.objects.filter(post_id=post_id).select_related("author")
