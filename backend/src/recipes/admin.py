from django.contrib import admin

from src.recipes.models import IngredientAmount, Recipe, UserRecipeRelation


class IngredientAmountInline(admin.TabularInline):
    """Добавление ингредиентов в рецепт."""

    model = IngredientAmount
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты."""

    list_display = ('id', 'name', 'author', 'favorited_count')
    list_display_links = ('name',)
    list_filter = ('tags',)
    search_fields = ('name', 'author__username', 'tags__name')
    readonly_fields = ('favorited_count',)
    exclude = ('ingredients',)
    inlines = [IngredientAmountInline]
    save_on_top = True

    def favorited_count(self, obj):
        return obj.readers_recipe.filter(favourites=True).count()

    favorited_count.short_description = 'В избранном'


@admin.register(UserRecipeRelation)
class UserRecipeRelationAdmin(admin.ModelAdmin):
    """Рецепты сохраненные у пользователя."""

    list_display = ('id', 'user', 'recipe', 'favourites', 'purchases')
    list_display_links = ('user',)
    list_filter = ('favourites', 'purchases')
    search_fields = ('recipe__name', 'user__username')
