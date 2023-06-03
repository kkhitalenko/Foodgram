from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ORM model for users."""

    email = models.EmailField('email', max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
