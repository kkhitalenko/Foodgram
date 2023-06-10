from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import serializers
from users.models import User

STANDART_USER_FIELDS = ('email', 'id', 'username', 'first_name', 'last_name',)


class CustomUserSerializer(UserSerializer):
    """Serializer for users viewing."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = STANDART_USER_FIELDS + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return obj.author.filter(
            subscriber=self.context.get('request').user.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer for creating new users."""

    class Meta:
        model = User
        fields = STANDART_USER_FIELDS + ('password',)


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer for subscriptions."""

    class Meta(CustomUserSerializer.Meta):
        # fields = + ( 'is_subscribed', 'recipes', "recipes", 'recipes_count')
        fields = STANDART_USER_FIELDS + ('is_subscribed',)
        read_only_fields = STANDART_USER_FIELDS + ('is_subscribed',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for getting ingredients."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer for creating Ingredient-Recipe relationship."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.ingredient')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'ingredient', 'measurement_unit', 'amount')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for adding ingredients in recipe."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeViewSerializer(serializers.ModelSerializer):
    """Serializer of GET method for /recipes/ and /recipes/id/ endpoints."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientSerializer(many=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'is_in_shopping_cart', 'name', 'image', 'text',
        #           'cooking_time')
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')

    # def get_is_favorite():

    # def get_is_in_shopping_cart():


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer of POST, PATCH, DELETE methods for /recipes/ and
    /recipes/{id}/ endpoints."""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'is_in_shopping_cart', 'name', 'image', 'text',
        #           'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError('Укажите теги')
        if not ingredients:
            raise serializers.ValidationError('Укажите ингридиенты')
        ingredients_list = []
        for ingredient in ingredients:
            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError({
                    'amount': 'Укажите количество ингридиента'})
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError({
                    'ingredient': 'Ингредиент уже добавлен'})
            ingredients_list.append(ingredient['id'])
        return data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        ingredients_in_recipe_list = []
        for i in ingredients:
            ingredient = Ingredient.objects.get(pk=i['id'])
            ingredients_in_recipe_list.append(
                IngredientInRecipe(recipe=recipe, ingredient=ingredient,
                                   amount=i['amount']))
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipe_list)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            self.add_ingredients(instance, ingredients)
        return super().update(instance, validated_data)
