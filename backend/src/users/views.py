from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.base.pagination import CustomPagination
from src.users.models import Follow, User
from src.users.serializers import FollowSerializer, UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
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
        serializer = FollowSerializer(
            self.paginate_queryset(request.user.follower.all()),
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=('post', 'delete'),
            url_path='subscribe',
            detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk):
        """Подписаться/отписаться от пользователя."""
        author = get_object_or_404(User, id=pk)
        user = request.user
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'error': 'Нельзя подписываться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST)
            if not user.follower.filter(author=author).exists():
                subscription = Follow.objects.create(user=user, author=author)
                serializer = FollowSerializer(
                    subscription,
                    context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Вы же уже подписаны на автора!'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription = get_object_or_404(Follow, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
