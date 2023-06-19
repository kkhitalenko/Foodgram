import json

from django.core.management.base import BaseCommand

from api.serializers import IngredientSerializer

filepath = 'data/ingredients.json'


class Command(BaseCommand):
    help = "Import ingredients from ingredients.json."

    def handle(self, *args, **options):
        try:
            with open(filepath, encoding='utf-8') as json_file:
                ingredients = json.load(json_file)
                for ingredient in ingredients:
                    serializer = IngredientSerializer(data=ingredient)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        self.stdout.write(self.style.SUCCESS(
                            f'Ошибка в файле {serializer.errors}'
                        ))
                self.stdout.write(self.style.SUCCESS('Файл успешно загружен'))
        except Exception as e:
            raise Exception(f'Ошибка: {e}')
