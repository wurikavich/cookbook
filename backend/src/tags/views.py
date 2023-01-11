from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer
from ..base.filters import RecipeFilter
from ..base.permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """CRUD Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_class = RecipeFilter
