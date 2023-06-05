import csv

from django.core.management.base import BaseCommand

from ...models import Ingredient


def ingredients_data():
    with open('data/ingredients.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Ингредиенты были добавлены.')


class Command(BaseCommand):
    help = 'Команда для загрузки данных в базу'

    def handle(self, *args, **options):
        funcs = [
            ingredients_data,
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
