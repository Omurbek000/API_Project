from django.db import models
from django.contrib.auth.models import User


# Категории постов
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.title


# Посты
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.author.username}"


# Комментарии
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username}"


# Избранное
class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} → {self.post.title}"
