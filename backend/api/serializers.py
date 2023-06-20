from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription, User

from .constants import STANDART_USER_FIELDS


class CustomUserSerializer(UserSerializer):
    """Serializer for users viewing."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = STANDART_USER_FIELDS + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            subscriber=request.user, author=obj.id
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer for creating new users."""

    class Meta:
        model = User
        fields = STANDART_USER_FIELDS + ('password',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for getting ingredients."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient-Recipe relationship."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for adding ingredients in recipe."""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer for subscriptions."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = STANDART_USER_FIELDS + ('is_subscribed', 'recipes',
                                         'recipes_count')
        read_only_fields = fields

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = Recipe.objects.filter(author=obj)
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            queryset = queryset[:int(recipes_limit)]
        serializer = AddToFavoriteOrShoppingCartSerializer(
            queryset, many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class RecipeViewSerializer(serializers.ModelSerializer):
    """Serializer of GET method for /recipes/ and /recipes/id/ endpoints."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='ingredient_in_recipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user,
                                           recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return ShoppingCart.objects.filter(user=request.user,
                                               recipe_id=obj.id).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer of POST, PATCH, DELETE methods for /recipes/ and
    /recipes/{id}/ endpoints."""

    ingredients = IngredientInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError('Укажите теги')
        if not ingredients:
            raise serializers.ValidationError('Укажите ингридиенты')
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError({
                    'ingredient': 'Ингредиент уже добавлен'
                })
            ingredients_list.append(ingredient['id'])
        return data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        ingredients_in_recipe_list = []
        for i in ingredients:
            ingredient = Ingredient.objects.get(pk=i['id'])
            amount = i['amount']
            ingredients_in_recipe_list.append(
                IngredientInRecipe(ingredient=ingredient, recipe=recipe,
                                   amount=amount)
            )
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipe_list)

    @transaction.atomic()
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic()
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            self.add_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeViewSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class AddToFavoriteOrShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for adding to favorite or shopping cart."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields
