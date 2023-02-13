from django.contrib import admin

from src.ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты."""

    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = search_fields = ('name',)
    list_filter = ('measurement_unit',)
