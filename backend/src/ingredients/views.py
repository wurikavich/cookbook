from rest_framework import viewsets

from src.base.filters import IngredientSearchFilter
from src.base.permissions import IsAdminOrReadOnly
from src.ingredients.models import Ingredient
from src.ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """CRUD ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None
