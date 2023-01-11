from django.contrib import admin

from .models import Favourite, Ingredient, IngredientRecipe, Purchases, Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты."""
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = search_fields = ('name',)
    list_filter = ('measurement_unit',)


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
    exclude = ('ingredients',)
    inlines = [IngredientAmountInline]
    search_fields = ('author__username', 'name', 'tags__name')
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


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    """Рецепты добавленные в избранное."""
    list_display = ('id', 'user', 'recipe', 'add_date')
    list_display_links = ('user',)
    search_fields = ('user', 'recipe')


@admin.register(Purchases)
class PurchasesAdmin(admin.ModelAdmin):
    """Рецепты добавленные в список покупок."""
    list_display = ('id', 'user', 'recipe', 'add_date')
    list_display_links = ('user',)
    search_fields = ('user', 'recipe')
