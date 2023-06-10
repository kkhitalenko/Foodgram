from django.contrib import admin
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
    # list_display = ('id', 'author', 'name', 'added_to_favorite')
    list_filter = ('author', 'name', 'tags')

    inlines = (IngredientInRecipeInline,)

    # @admin.display(description='Добавлено в избранное')
    # def added_to_favorite(self, obj):
    #     return ...
