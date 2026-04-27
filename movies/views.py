from urllib import request

from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking, Genre, Language
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Count, Q


def movie_list(request):
    genres = request.GET.getlist('genres')
    languages = request.GET.getlist('languages')
    search_query = request.GET.get('search')

    sort = request.GET.get('sort', 'release_date')

    movies = Movie.objects.all()

    # 🔍 FILTERING
    if search_query:
        movies = movies.filter(name__icontains=search_query)

    if genres:
        movies = movies.filter(genres__id__in=genres).distinct()

    if languages:
        movies = movies.filter(languages__id__in=languages).distinct()

    # ✅ IMPORTANT: capture BEFORE sorting/pagination
    filtered_movies = movies

    # 🔽 SORTING
    allowed_sorts = ['release_date', 'rating', 'title']
    if sort not in allowed_sorts:
        sort = 'release_date'

    movies = movies.order_by(sort)

    # ⚡ OPTIMIZATION
    movies = movies.prefetch_related('genres', 'languages')

    # 🎯 COUNTS (FIXED)
    genre_counts = Genre.objects.annotate(
        movie_count=Count('movies', filter=Q(movies__in=filtered_movies))
    )

    language_counts = Language.objects.annotate(
        movie_count=Count('movies', filter=Q(movies__in=filtered_movies))
    )

    # 📄 PAGINATION
    paginator = Paginator(movies, 10)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    return render(request, 'movies/movie_list.html', {
        'movie': movies,
        'selected_genres': genres,
        'selected_languages': languages,
        'selected_sort': sort,
        'search_query': search_query,
        'genre_counts': genre_counts,
        'language_counts': language_counts
    })

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        error_seats=[]
        if not selected_Seats:
            return render(request,"movies/seat_selection.html",{'theater':theater,"seats":seats,'error':"No seat selected"})
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked=True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats:
            error_message=f"The following seats are already booked:{',',join(error_seats)}"
            return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':"No seat selected"})
        return redirect('profile')
    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    theaters = movie.theaters.all()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'theaters': theaters
    })