import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


def ingredients_data():
    with open('data/ingredients.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for name, measurement_unit in reader:
            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit
            )
        print('Ингредиенты были добавлены.')

def create_tags():
    tags=(
        'Завтрак', 'green', 'breakfast',
        'Обед', 'blue', 'Lunch',
        'Ужин', 'red', 'Dinner',
    )
    for name, color, slug in tags:
        Tag.objects.get_or_create(
                name=name,
                color=color,
                slug=slug
            )
        print('Тэги были добавлены.')


class Command(BaseCommand):
    help = 'Команда для загрузки данных в базу'

    def handle(self, *args, **options):
        funcs = [
            ingredients_data,
            create_tags
        ]
        for func in funcs:
            try:
                func()
            except FileNotFoundError:
                print(
                    FileNotFoundError(
                        f'Файл {func.__name__[:-5]}.csv не найден!'
                    )
                )

