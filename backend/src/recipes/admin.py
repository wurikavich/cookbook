from django.contrib import admin

from src.recipes.models import Favourite, IngredientRecipe, Purchases, Recipe


@admin.register(Purchases)
@admin.register(Favourite)
class BaseAdminControl(admin.ModelAdmin):
    """Базовая админ панель для моделей: Favourite, Purchases."""
    list_display = ('id', 'user', 'recipe', 'add_date')
    list_display_links = ('user',)
    search_fields = ('user', 'recipe')


class IngredientAmountInline(admin.TabularInline):
    """Добавление ингредиентов в рецепт."""
    model = IngredientRecipe
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
        return Favourite.objects.filter(recipe=obj).count()

    favorited_count.short_description = 'В избранном'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Количество ингредиентов в рецепте."""
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_display_links = ('recipe',)
    search_fields = ('name',)
