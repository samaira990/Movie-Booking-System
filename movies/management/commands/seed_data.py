import random
from datetime import date
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Language


class Command(BaseCommand):
    help = "Fast seed 500 movies"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old movies...")
        Movie.objects.all().delete()

        genres = list(Genre.objects.all())
        languages = list(Language.objects.all())

        self.stdout.write("Creating movies (bulk)...")

        movies_to_create = []

        for i in range(1, 51):
            movies_to_create.append(
                Movie(
                    name=f"Movie {i}",
                    rating=round(random.uniform(5.0, 9.5), 1),
                    cast="Actor A, Actor B",
                    description=f"This is movie number {i}",
                    release_date=date(2020, 1, 1),
                )
            )

        # 🚀 BULK CREATE (FAST)
        created_movies = Movie.objects.bulk_create(movies_to_create)

        self.stdout.write("Assigning genres & languages...")

        for movie in created_movies:
            movie.genres.add(*random.sample(genres, k=2))
            movie.languages.add(*random.sample(languages, k=1))

        self.stdout.write(self.style.SUCCESS("500 movies seeded successfully 🚀"))