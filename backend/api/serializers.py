from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Tag
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
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
