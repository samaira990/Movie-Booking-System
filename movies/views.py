from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking, Genre, Language
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Q
from django.core.paginator import Paginator


def movie_list(request):
    movies = Movie.objects.all().prefetch_related(
        'genres',
        'languages'
    )

    # 🔍 SEARCH
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(
            name__icontains=search_query
        )

    # 🎭 GENRES FILTER
    selected_genres = request.GET.getlist('genres')
    if selected_genres:
        movies = movies.filter(
            genres__id__in=selected_genres
        ).distinct()

    # 🌐 LANGUAGES FILTER
    selected_languages = request.GET.getlist('languages')
    if selected_languages:
        movies = movies.filter(
            languages__id__in=selected_languages
        ).distinct()

    # 🔽 SORTING
    selected_sort = request.GET.get(
        'sort',
        'name'
    )

    if selected_sort == 'rating':
        movies = movies.order_by(
            '-rating'
        )
    else:
        movies = movies.order_by(
            'name'
        )

    # 🚀 PAGINATION
    paginator = Paginator(
        movies,
        12
    )

    page_number = request.GET.get(
        'page'
    )

    movies = paginator.get_page(
        page_number
    )

    # 📊 COUNTS
    genre_counts = Genre.objects.annotate(
        movie_count=Count(
            'movies',
            filter=Q(
                movies__isnull=False
            ),
            distinct=True
        )
    )

    language_counts = Language.objects.annotate(
        movie_count=Count(
            'movies',
            filter=Q(
                movies__isnull=False
            ),
            distinct=True
        )
    )

    # Preserve filters in pagination
    query_params = request.GET.copy()
    query_params.pop(
        'page',
        None
    )

    return render(
        request,
        'movies/movie_list.html',
        {
            'movies': movies,
            'genre_counts': genre_counts,
            'language_counts': language_counts,
            'selected_genres': selected_genres,
            'selected_languages': selected_languages,
            'selected_sort': selected_sort,
            'search_query': search_query,
            'query_params': query_params.urlencode(),
        }
    )

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)

    return render(request, 'movies/theater_list.html', {
        'movie': movie,
        'theaters': theaters
    })


@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theater,
                "seats": seats,
                'error': "No seat selected"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)

            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()

            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {
                'theater': theater,
                "seats": seats,
                'error': error_message
            })

        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {
        'theater': theater,
        "seats": seats
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = movie.theaters.all()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'theaters': theaters
    })