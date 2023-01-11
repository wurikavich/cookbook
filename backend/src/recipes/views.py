from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Favourite, Ingredient, IngredientRecipe, Purchases, Recipe
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer, RecipeReadSerializer)
from ..base.filters import IngredientSearchFilter, RecipeFilter
from ..base.pagination import CustomPagination
from ..base.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from ..base.utils import add_object, create_pdf_file, delete_object


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """CRUD ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """CRUD рецептов."""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Переопределение выбора сериализатора."""
        if self.action in ('retrieve', 'list'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(methods=('post', 'delete'),
            detail=True,
            url_path='favorite',
            permission_classes=(IsAuthenticated,))
    def set_favorite(self, request, pk):
        """Добавить/удалить рецепт в избранном."""
        if request.method == 'POST':
            return add_object(Favourite, request.user, pk)
        return delete_object(Favourite, request.user, pk)

    @action(detail=True,
            methods=('post', 'delete'),
            url_path='shopping_cart',
            permission_classes=(IsAuthenticated,))
    def set_shopping_cart(self, request, pk):
        """Добавить/удалить рецепт в список покупок."""
        if request.method == 'POST':
            return add_object(Purchases, request.user, pk)
        return delete_object(Purchases, request.user, pk)

    @action(detail=False,
            methods=('get',),
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def set_download_shopping_cart(self, request):
        """Собрать необходимые данные для формирования список покупок."""
        recipes = Recipe.objects.filter(
            id__in=request.user.purchases.values_list('recipe', flat=True))
        shopping_list = {}
        for recipe in recipes:
            ingredients = IngredientRecipe.objects.filter(recipe=recipe)
            for ing in ingredients:
                if ing.ingredient.name in shopping_list:
                    shopping_list[ing.ingredient.name][0] += ing.amount
                else:
                    shopping_list[ing.ingredient.name] = [
                        ing.amount,
                        ing.ingredient.measurement_unit]
        return create_pdf_file(shopping_list)