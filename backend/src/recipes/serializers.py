from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from src.ingredients.models import Ingredient
from src.recipes.models import IngredientAmount, Recipe, UserRecipeRelation
from src.tags.models import Tag
from src.tags.serializers import TagSerializer
from src.users.serializers import UserSerializer


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Вывод необходимых полей ингредиента при запросе рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        source='ingredient', slug_field='name', read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient', slug_field='measurement_unit', read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Вывод информации о рецепте."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientAmountSerializer(
        source='amounts', many=True, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class RecipeCreateSerializer(RecipeReadSerializer):
    """CRUD рецептов."""

    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            IngredientAmount.objects.filter(recipe=instance).delete()
            self.add_ingredients(instance, ingredients)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        if len(tags) < 1:
            raise ValidationError('В рецепте не указаны Теги!')
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError('Теги повторяются!')
            tags_list.append(tag)

        if len(ingredients) < 1:
            raise ValidationError('В рецепте не указаны ингредиенты!')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise ValidationError('Ингредиенты повторяются!')
            ingredients_list.append(ingredient_id)

        return data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient']
            ) for ingredient in ingredients])

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class UserRecipeRelationSerializer(serializers.ModelSerializer):
    """Валидация данных при добавлении рецепта в избранное или корзину."""

    class Meta:
        model = UserRecipeRelation
        fields = ('user', 'recipe', 'favourites', 'purchases')

    def validate(self, data):
        recipe = data.get('recipe')
        user = data.get('user')
        favourites = data.get('favourites')
        purchases = data.get('purchases')
        if favourites and user.readers_user.filter(recipe=recipe,
                                                   favourites=True).exists():
            raise ValidationError('Рецепт уже добавлен!')
        if purchases and user.readers_user.filter(recipe=recipe,
                                                  purchases=True).exists():
            raise ValidationError('Рецепт уже добавлен!')
        return data
