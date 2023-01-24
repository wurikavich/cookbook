from rest_framework import serializers

from src.base.serializers import RecipeShortInfoSerializer
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


class FollowCreateSerializer(serializers.ModelSerializer):
    """Валидация данных при создании подписки."""

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user.follower.filter(author=author).exists():
            raise serializers.ValidationError('Вы же уже подписаны на автора!')
        if user == author:
            raise serializers.ValidationError('Нельзя подписываться на себя!')
        return data


class FollowReadSerializer(serializers.ModelSerializer):
    """Вывод подписок пользователей."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes_count = serializers.IntegerField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(
        source='get_is_subscribed',
        read_only=True)
    recipes = serializers.SerializerMethodField(
        source='get_recipes',
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
        return RecipeShortInfoSerializer(queryset, many=True).data
