import random
from datetime import date
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Language


class Command(BaseCommand):
    help = "Seed 500 movies"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old movies...")

        Movie.objects.all().delete()

        # Ensure genres/languages exist
        if Genre.objects.count() == 0:
            genres = [
                Genre.objects.create(name="Action"),
                Genre.objects.create(name="Drama"),
                Genre.objects.create(name="Comedy"),
                Genre.objects.create(name="Sci-Fi"),
                Genre.objects.create(name="Romance"),
            ]
        else:
            genres = list(Genre.objects.all())

        if Language.objects.count() == 0:
            languages = [
                Language.objects.create(name="English"),
                Language.objects.create(name="Hindi"),
                Language.objects.create(name="Tamil"),
            ]
        else:
            languages = list(Language.objects.all())

        self.stdout.write("Creating 500 movies...")

        for i in range(1, 501):
            movie = Movie.objects.create(
                name=f"Movie {i}",
                rating=round(random.uniform(5.0, 9.5), 1),
                cast="Actor A, Actor B",
                description=f"This is movie number {i}",
                release_date=date(2020, 1, 1),
            )

            movie.genres.add(*random.sample(genres, k=2))
            movie.languages.add(*random.sample(languages, k=1))

        self.stdout.write(self.style.SUCCESS("500 movies created successfully 🎬"))