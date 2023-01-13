from rest_framework import viewsets

from src.base.filters import RecipeFilter
from src.base.permissions import IsAdminOrReadOnly
from src.tags.models import Tag
from src.tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """CRUD Тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_class = RecipeFilter
    pagination_class = None
