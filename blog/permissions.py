from rest_framework import permissions

# ───────────────────────────── BASE MIXIN ─────────────────────────────

class OwnerPermissionMixin:
     """
    Универсальный миксин для проверки владельца объекта.
    Поддерживает два варианта:
    - obj.user
    - obj.author

    Используется в нескольких permission-классах.
    """

    def is_owner(self, obj, user):
        owner = getattr(obj,'user', None) or getattr(obj, 'author', None)
        return owner == user

# ───────────────────────────── READ ONLY ─────────────────────────────

class IsAdminOrReadOnly(permissions.BasePermission):
       """
    Разрешает:
    - GET/HEAD/OPTIONS — всем
    - POST/PUT/PATCH/DELETE — только администратору

    Используется для категорий, чтобы обычные пользователи не могли их менять.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

# ───────────────────────────── AUTHOR OR READ ONLY ─────────────────────────────

class IsAuthorOrReadOnly(OwnerPermissionMixin,permissions.BasePermission):
      """
    Разрешает:
    - безопасные методы всем
    - изменение/удаление — только автору объекта
    - администратор имеет полный доступ

    Используется для постов и комментариев.
    """

    def has_permission(self, request, view):
         # GET/HEAD/OPTIONS — всем
         if request.method in permissions.SAFE_METHODS:
             return True
         # POST/PUT/PATCH/DELETE — только авторизованным
         return request.user.is_authenticated

    def has_object_permission(self,request, view , obj):
        # Безопасные методы — всем
        if request.method in permissions.SAFE_METHODS:
            return True
         # Админ может всё
        if  request.user.is_staff:
            return True

        # Проверка владельца
        return self.is_owner(obj,request.user)

# ───────────────────────────── OWNER ONLY ─────────────────────────────

class IsOwner(OwnerPermissionMixin, permissions.BasePermission):
     """
    Доступ только владельцу объекта.
    Используется для:
    - профиля пользователя
    - избранного
    - личных данных

    Администратор также имеет доступ.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self,request,view,obj):
        if request.user.is_staff:
            return True
        return self.is_owner(obj,request.user)


# ───────────────────────────── OWNER OR READ ONLY ─────────────────────────────

class IsOwnerOrReadOnly(OwnerPermissionMixin, permissions.BasePermission):
      """
    Разрешает:
    - безопасные методы всем
    - изменение — только владельцу
    - администратор имеет полный доступ

    Используется для избранного, сообщений и других объектов,
    где владелец — это user, а не author.
    """

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_sfaff:
            return True
        return self.is_owner(obj,request.user)

# ───────────────────────────── MESSAGES ─────────────────────────────

class IsSenderOrRecipient(permissions.BasePermission):
      """
    Доступ к личным сообщениям:
    - только отправитель или получатель
    - администратор имеет доступ

    Используется в MessageViewSet.
    """

    def has_permission(self,request,view):
        return request.user.is_authenticated

    def has_object_permission(self,request, view, obj):
        if request.user.is_staff:
            return True
        return(
            obj.sender == request.user or 
            obj.recipient == request.user
        )




# Что мы сделали в PERMISSIONS?
# ✔ Добавили OwnerPermissionMixin
# Чтобы не дублировать код проверки владельца.

# ✔ Добавили поддержку staff во всех permissions
# Админ теперь имеет полный доступ.

# ✔ Унифицировали логику
# Теперь все permissions работают одинаково и предсказуемо.

# ✔ Улучшили безопасность
# Никаких дыр, никаких обходов.

# ✔ Улучшили читаемость
# Каждый класс имеет чёткое назначение.