from api.filters import IngredientSearch, RecipeFilter
from api.pagination import StandardResultsSetPagination
from api.permissions import RecipePermission
from api.serializers import (AddToFavoriteOrShoppingCartSerializer,
                             IngredientSerializer,
                             RecipeCreateUpdateSerializer,
                             RecipeViewSerializer, SubscriptionSerializer,
                             TagSerializer)
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
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
            return Response(
                {'errors': f'Вы не подписаны на {author.username}'},
                status=status.HTTP_400_BAD_REQUEST)

        if subscription.exists():
            return Response(
                {'errors': f'Вы уже подписаны на {author.username}'},
                status=status.HTTP_400_BAD_REQUEST)
        if author == subscriber:
            return Response({'errors': 'Невозможно подписаться на себя'},
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
    filter_backends = [IngredientSearch]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for recipes."""

    queryset = Recipe.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [RecipePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeViewSerializer
        return RecipeCreateUpdateSerializer

    @staticmethod
    def add(pk, model, user):
        recipe = Recipe.objects.get(id=pk)
        object = model.objects.filter(user=user, recipe_id=pk)
        if object.exists():
            return Response({'errors': f'Вы уже добавили {recipe}'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = AddToFavoriteOrShoppingCartSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_recipe(pk, model, user):
        recipe = Recipe.objects.get(id=pk)
        object = model.objects.filter(user=user, recipe_id=pk)
        if object.exists():
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': f'Вы не добавляли {recipe}'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'DELETE':
            return self.delete_recipe(pk, Favorite, user)
        return self.add(pk, Favorite, user)

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'DELETE':
            return self.delete_recipe(pk, ShoppingCart, user)
        return self.add(pk, ShoppingCart, user)

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        header = 'Cписок покупок'
        for index, ingredient in enumerate(ingredients):
            name = ingredient['ingredient__name']
            amount = ingredient['amount']
            current_ingredient = ingredient['ingredient__measurement_unit']
            header += f'\n {name}: {amount} {current_ingredient}'
            if index < ingredients.count() - 1:
                header += ','
        file = 'shopping_cart'
        response = HttpResponse(header, 'Content-Type: application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response
