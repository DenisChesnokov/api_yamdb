import csv

from django.core.management.base import BaseCommand
from reviews.models import Genres, Title, TitleGenres

from api_yamdb.settings import IMPORT_DATA_ADRESS


class Command(BaseCommand):
    help = 'Импортирует базу данных для связей Genres-Title из файла csv'

    def handle(self, *args, **options):

        with open(
            f'{IMPORT_DATA_ADRESS}/genre_title.csv',
            'r', encoding="utf-8-sig"
        ) as csv_file:
            dataReader = csv.DictReader(csv_file)

            for row in dataReader:
                try:
                    title_genre = TitleGenres()
                    title_genre.id = row['id']
                    title_id = row['title_id']
                    genre_id = row['genre_id']
                    title_genre.title = Title.objects.get(id=title_id)
                    title_genre.genre = Genres.objects.get(id=genre_id)
                
                    if TitleGenres.objects.filter(id=title_genre.id).exists():
                        self.stdout.write(
                            f'Связь c id {title_genre.id}'
                            f'уже существует в базе.'
                        )

                    elif TitleGenres.objects.filter(
                        title=title_genre.title, genre=title_genre.genre
                    ).exists():
                        self.stdout.write(
                            f'Связь {title_genre.title.name} -'
                            f'{title_genre.genre.name} уже существует в базе.'
                        )

                    else:
                        title_genre.save()

                        self.stdout.write(
                            f'Связь "{title_genre.title.name} -'
                            f'{title_genre.genre.name}" внесена в базу.'
                        )
