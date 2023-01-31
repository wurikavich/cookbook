from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Доступы для моделей: Tag, Ingredient
    Разрешить:
        Чтение: Всем пользователям
        Полный доступ: Администраторы
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_staff)
        )


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Доступы для моделей: Recipe
    Разрешить:
        Чтение: Всем пользователям
        POST DELETE PATCH: Авторам рецепта
        Полный доступ: Администраторы
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            obj.author == request.user or
            request.user.is_staff
        )
