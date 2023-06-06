from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    # is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        # fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id',  'username', 'first_name', 'last_name', 'password'
        )
