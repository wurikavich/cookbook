from rest_framework import serializers

from src.recipes.models import Recipe
from src.users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """Вывод информации о пользователях."""

    is_subscribed = serializers.SerializerMethodField(
        read_only=True,
        source='get_is_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or (request.user == obj):
            return False
        return request.user.follower.filter(author=obj).exists()


class RecipeShortSerializer(serializers.ModelSerializer):
    """"Вывод необходимых полей рецепта для отображения в профиле юзера."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Вывод подписок пользователей."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        source='get_is_subscribed',
        read_only=True)
    recipes = serializers.SerializerMethodField(
        source='get_recipes',
        read_only=True)
    recipes_count = serializers.SerializerMethodField(
        source='get_recipes_count',
        read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or (request.user == obj.author):
            return False
        return request.user.follower.filter(author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            try:
                queryset = queryset[:int(recipes_limit)]
            except ValueError:
                raise ValueError(f'Некорректное значение - {recipes_limit}')
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
