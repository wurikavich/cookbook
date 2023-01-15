from rest_framework import serializers

from src.recipes.models import Recipe


class RecipeShortInfoSerializer(serializers.ModelSerializer):
    """"Вывод необходимых полей рецепта для отображения в профиле юзера."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
