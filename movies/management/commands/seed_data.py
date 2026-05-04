from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Language
from datetime import date


class Command(BaseCommand):
    help = "Seed database with movies, genres, and languages"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")

        Movie.objects.all().delete()
        Genre.objects.all().delete()
        Language.objects.all().delete()

        self.stdout.write("Creating genres and languages...")

        # 🎭 Genres
        action = Genre.objects.create(name="Action")
        drama = Genre.objects.create(name="Drama")
        scifi = Genre.objects.create(name="Sci-Fi")
        romance = Genre.objects.create(name="Romance")

        # 🌐 Languages
        hindi = Language.objects.create(name="Hindi")
        english = Language.objects.create(name="English")

        self.stdout.write("Creating movies...")

        movie1 = Movie.objects.create(
            name="Avengers: Endgame",
            rating=8.4,
            cast="Robert Downey Jr., Chris Evans, Scarlett Johansson",
            description="Avengers assemble to reverse Thanos' snap.",
            release_date=date(2019, 4, 26),
        )
        movie1.genres.add(action, scifi)
        movie1.languages.add(english)

        movie2 = Movie.objects.create(
            name="Inception",
            rating=8.8,
            cast="Leonardo DiCaprio, Joseph Gordon-Levitt",
            description="A thief enters dreams to plant an idea.",
            release_date=date(2010, 7, 16),
        )
        movie2.genres.add(scifi, drama)
        movie2.languages.add(english)

        movie3 = Movie.objects.create(
            name="Titanic",
            rating=7.9,
            cast="Leonardo DiCaprio, Kate Winslet",
            description="A love story on the ill-fated Titanic ship.",
            release_date=date(1997, 12, 19),
        )
        movie3.genres.add(romance, drama)
        movie3.languages.add(english, hindi)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully 🎬"))