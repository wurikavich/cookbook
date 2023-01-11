from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .utils import get_queryset
from ..recipes.models import Recipe
from ..tags.models import Tag
from ..users.models import User


class IngredientSearchFilter(SearchFilter):
    """Поиск ингредиента по названию."""

    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """Поиск рецептов и тегов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        label='Tags')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_is_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        return get_queryset(queryset, value, self.request.user.favorites)

    def get_is_shopping_cart(self, queryset, name, value):
        return get_queryset(queryset, value, self.request.user.purchases)