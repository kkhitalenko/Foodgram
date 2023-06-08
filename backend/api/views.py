from api.filters import IngredientSearch
from api.pagination import StandardResultsSetPagination
from api.serializers import (IngredientSerializer, SubscriptionSerializer,
                             TagSerializer)
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Ingredient, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    """ViewSet for users."""

    pagination_class = StandardResultsSetPagination

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        subscription = Subscription.objects.filter(subscriber=subscriber,
                                                   author=author)
        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response((f'Вы не подписаны на {author.username}'),
                            status=status.HTTP_400_BAD_REQUEST)

        if subscription.exists():
            return Response((f'Вы уже подписаны на {author.username}'),
                            status=status.HTTP_400_BAD_REQUEST)
        if author == subscriber:
            return Response('Невозможно подписаться на себя',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionSerializer(author, data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(subscriber=subscriber, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(author__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, context={'request': request},
                                            many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ingredients."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = (IngredientSearch,)
    search_fields = ('^name',)
