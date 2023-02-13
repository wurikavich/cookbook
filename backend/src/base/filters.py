from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from src.recipes.models import Recipe
from src.tags.models import Tag
from src.users.models import User


class IngredientSearchFilter(SearchFilter):
    """Поиск ингредиентов по названию."""

    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """Поиск рецептов и тегов."""

    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_bool')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_bool')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        label='Tags'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    @staticmethod
    def filter_bool(queryset, name, value):
        if value:
            return queryset.filter(**{name: value})
        return queryset
