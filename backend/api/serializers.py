from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User

STANDART_FIELDS = ('email', 'id', 'username', 'first_name', 'last_name',)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = STANDART_FIELDS + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return obj.author.filter(
            subscriber=self.context.get('request').user.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = STANDART_FIELDS + ('password',)


class SubscriptionSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        # fields = ('id', 'email', 'username', 'first_name',
        #           'last_name', 'is_subscribed', 'recipes', "recipes", 'recipes_count')
        fields = STANDART_FIELDS + ('is_subscribed',)
        read_only_fields = STANDART_FIELDS + ('is_subscribed',)
