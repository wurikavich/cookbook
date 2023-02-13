from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.base.pagination import CustomPagination
from src.users.models import Follow, User
from src.users.serializers import (
    FollowCreateSerializer,
    FollowReadSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.GenericViewSet):
    """CRUD пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    search_fields = ('username',)

    @action(methods=('get',),
            url_path='subscriptions',
            detail=False,
            permission_classes=(IsAuthenticated,))
    def get_subscriptions(self, request):
        """Возвращает список подписок пользователя."""
        queryset = self.paginate_queryset(
            request.user.follower.all()
            .annotate(recipes_count=Count('author__recipes'))
            .order_by('id')
        )
        serializer = FollowReadSerializer(
            queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('post', 'delete'),
            url_path='subscribe',
            detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk):
        """Подписаться/отписаться от пользователя."""
        if request.method == 'POST':
            data = {
                'user': request.user.id,
                'author': pk
            }
            context = {'request': request}
            serializer = FollowCreateSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            subscription = serializer.save()
            serializer = FollowReadSerializer(subscription, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        author = get_object_or_404(User, id=pk)
        obj = get_object_or_404(Follow, user=request.user, author=author)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
