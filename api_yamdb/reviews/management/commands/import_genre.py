import csv

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from reviews.models import Genres

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для модели Genres из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/genre.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:

                try:
                    genre_name = row['name']

                    Genres.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )

                except IntegrityError as err:
                    self.stdout.write(
                        f'Жанр {genre_name} уже внесен в базу. '
                        f'Ошибка внесения - {err}'
                    )

                else:
                    self.stdout.write(
                        f'Жанр {genre_name} внесен в базу.'
                    )
