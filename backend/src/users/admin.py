from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from src.users.models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Управление пользователями."""

    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    )
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'recipes_count'
    )
    list_display_links = ('username',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    save_on_top = True

    def recipes_count(self, obj):
        return obj.recipes.count()

    recipes_count.short_description = 'Рецептов'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Управление подписками."""

    list_display = ('id', 'user', 'author')
    list_display_links = ('user',)
    search_fields = ('user__username',)
