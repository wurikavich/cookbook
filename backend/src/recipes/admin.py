from django.contrib import admin

from src.recipes.models import IngredientAmount, Recipe, UserRecipeRelation


class IngredientAmountInline(admin.TabularInline):
    """Добавление ингредиентов в рецепт."""
    model = IngredientAmount
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    """Рецепты."""
    list_display = ('id', 'name', 'author', 'favorited_count')
    list_display_links = ('name',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('author__username', 'name', 'tags__name')
    readonly_fields = ('favorited_count',)
    exclude = ('ingredients',)
    inlines = [IngredientAmountInline]
    save_on_top = True

    def favorited_count(self, obj):
        return UserRecipeRelation.objects.filter(
            recipe=obj, favourites=True).count()

    favorited_count.short_description = 'В избранном'


@admin.register(IngredientAmount)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Количество ингредиентов в рецепте."""
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_display_links = ('recipe',)
    search_fields = ('ingredient__name', 'recipe__name')


@admin.register(UserRecipeRelation)
class UserRecipeRelationAdmin(admin.ModelAdmin):
    """Рецепты сохраненные у пользователя."""
    list_display = ('id', 'user', 'recipe', 'favourites', 'purchases')
    list_display_links = ('user',)
    list_filter = ('favourites', 'purchases')
    search_fields = ('recipe__name', 'user__username')
