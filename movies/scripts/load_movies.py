import random
from datetime import date, timedelta
from movies.models import Movie, Genre, Language

# Some sample words to generate nicer titles
WORDS = [
    "Shadow", "Rise", "Legend", "Mission", "Empire", "Storm",
    "Dragon", "Code", "Matrix", "Journey", "War", "Secret",
    "Night", "Fire", "Sky", "Echo", "Blade", "King", "Queen"
]

# Free placeholder posters (no signup needed)
POSTERS = [
    "https://picsum.photos/300/450?random=1",
    "https://picsum.photos/300/450?random=2",
    "https://picsum.photos/300/450?random=3",
    "https://picsum.photos/300/450?random=4",
    "https://picsum.photos/300/450?random=5",
]

CAST_NAMES = [
    "Actor A", "Actor B", "Actor C", "Actor D",
    "Actor E", "Actor F", "Actor G"
]

DESCRIPTIONS = [
    "An intense story of courage and survival.",
    "A heartwarming tale of love and friendship.",
    "A thrilling journey full of unexpected twists.",
    "A battle between good and evil unfolds.",
    "A story that will keep you on the edge."
]


def random_title():
    return f"{random.choice(WORDS)} {random.choice(WORDS)}"


def random_date():
    start = date(2015, 1, 1)
    end = date(2025, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def run():
    genres = list(Genre.objects.all())
    languages = list(Language.objects.all())

    if not genres or not languages:
        print("❌ Add genres and languages first.")
        return

    created = 0

    for i in range(500):
        movie = Movie.objects.create(
            name=f"{random_title()} {i}",
            image=random.choice(POSTERS),   # CloudinaryField accepts URL
            rating=round(random.uniform(5.0, 9.5), 1),
            cast=", ".join(random.sample(CAST_NAMES, 3)),
            description=random.choice(DESCRIPTIONS),
            release_date=random_date()
        )

        # assign 1–3 genres
        movie.genres.set(random.sample(genres, k=random.randint(1, 3)))

        # assign 1–2 languages
        movie.languages.set(random.sample(languages, k=random.randint(1, 2)))

        created += 1

    print(f"✅ {created} movies created successfully!")