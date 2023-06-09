from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """ORM model for ingredient."""

    name = models.CharField(max_length=200, verbose_name='Ингридиент')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [models.UniqueConstraint(
            fields=('name', 'measurement_unit'),
            name='unique_ingredient_measurement_unit')]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ORM model for tag."""

    name = models.CharField(max_length=200, unique=True, verbose_name='Тег')
    color = models.CharField(max_length=7, unique=True, verbose_name='HEX-код')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ORM model for recipe."""

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe', verbose_name='Автор')
    name = models.CharField(max_length=200, verbose_name='Рецепт')
    image = models.ImageField(upload_to='images/', verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         related_name='recipe',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipe',
                                  verbose_name='Теги')
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время в минутах')
    pub_date = models.DateField(auto_now_add=True,
                                verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """ORM model for ingredients quantity in recipe."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_in_recipe',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient_in_recipe',
                               verbose_name='Рецепт')
    quantity = models.IntegerField(validators=[MinValueValidator(1)],
                                   verbose_name='Количество')

    class Meta:
        verbose_name = verbose_name_plural = 'Количество ингридиента в рецепте'
        constraints = [models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe')]

    def __str__(self):
        return f'{self.quantity}'
