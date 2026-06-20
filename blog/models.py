from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import Manager, QuerySet


User = get_user_model()


# ───────────────────────────── CATEGORY ─────────────────────────────
# Категории постов. Используются для фильтрации и группировки.
# Добавлен slug для SEO и красивых URL.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # Название категории
    slug = models.SlugField(max_length=120, unique=True, blank=True) # URL-идентификатор

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['slug']),]  # Ускоряет поиск по slug

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug, если он не указан
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


    
# ───────────────────────────── POST ─────────────────────────────
# Посты блога. Содержат текст, изображение, категорию и автора.
# Добавлены slug, excerpt, менеджеры, индексы, методы.

class PostQuerySet(QuerySet):
    # Фильтр опубликованных постов
    def published(self):
        return self.filter(status='published')

    # Фильтр постов конкретного автора

    def by_author(self,user):
        return self.filter(author=user)

class PostManager(Manager):
    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def by_author(self, user):
        return self.get_queryset().by_author(user)


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    ]

    title = models.CharField(max_length=200) # Заголовок
    slug = models.SlugField(max_length=220, unique=True, blank=True) # SEO URL
    text = models.TextField() #Полный текст
    excerpt = models.TextField(blank=True)  # Краткое описание
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) # Дата создания
    updated_at = models.DateTimeField(auto_now_add=True) # Дата Обновления 

    objects = PostManager() # Кастомный менеджер 

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        # Генерация slug
        if not self.slug:
            self.slug = slugify(self.title)

        # Генерация краткого описания 
        if not self.excerpt:
            self.excerpt = self.text[:200]

            super().save(*args, **kwargs)

    def increase_views(self):
        # Увеличение просмотров без гонки
        self.views = models.F('views') + 1
        self.save(update_fields=["view"]) 

    def __str__(self):
        return self.title

# ───────────────────────────── COMMENT ─────────────────────────────
# Комментарии к постам. Поддерживают древовидную структуру.
# Добавлен soft-delete.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blamk=True, related_name="replise")
    text = models.TextField()
    is_deleted = models.BooleanField(default=False) # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f"Комментарий от {self.author}"

# ───────────────────────────── FAVORITE ─────────────────────────────
# Избранные посты. Один пользователь — один пост.

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite_by')
    creted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_favorite")
        ]

    def __str__(self):
        return f"{self.user} → {self.post}"


# ───────────────────────────── MESSAGE ─────────────────────────────
# Личные сообщения между пользователями.
# Добавлен soft-delete для каждого участника.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.Foreign.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")

    text = models.TextField()
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_recipient = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["recipient"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.recipient}"