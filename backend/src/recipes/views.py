from django.db.models import Exists, OuterRef, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from src.base.filters import RecipeFilter
from src.base.pagination import CustomPagination
from src.base.permissions import IsAuthorOrAdminOrReadOnly
from src.recipes.models import IngredientAmount, Recipe
from src.recipes.serializers import (
    RecipeCreateSerializer, RecipeReadSerializer)
from src.recipes.utils import create_or_delete, create_pdf_file


class RecipeViewSet(viewsets.ModelViewSet):
    """CRUD рецептов."""
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.all().annotate(
                is_favorited=Exists(self.request.user.readers_user.filter(
                    recipe=OuterRef('id'), favourites=True)),
                is_in_shopping_cart=Exists(
                    self.request.user.readers_user.filter(
                        recipe=OuterRef('id'), purchases=True))
            ).select_related('author').prefetch_related('ingredients', 'tags')
        return Recipe.objects.all().select_related('author').prefetch_related(
            'ingredients', 'tags')

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

        return create_or_delete(request, pk, source='favourites')

    @action(detail=True,
            methods=('post', 'delete'),
            url_path='shopping_cart',
            permission_classes=(IsAuthenticated,))
    def set_shopping_cart(self, request, pk):
        """Добавить/удалить рецепт в список покупок."""

        return create_or_delete(request, pk, source='purchases')

    @action(detail=False,
            methods=('get',),
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def set_download_shopping_cart(self, request):
        """Собрать необходимые данные для формирования список покупок."""
        shopping_list = IngredientAmount.objects.filter(
            recipe__id__in=request.user.readers_user.filter(
                purchases=True).values_list('recipe', flat=True)
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        return create_pdf_file(shopping_list)
