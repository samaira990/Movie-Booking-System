from urllib import request

from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking, Genre, Language
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Count, Q


def movie_list(request):
    movies = Movie.objects.all()

    # 🔍 SEARCH
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(name__icontains=search_query)

    # 🎭 GENRES FILTER
    selected_genres = request.GET.getlist('genres')
    if selected_genres:
        movies = movies.filter(genre__id__in=selected_genres).distinct()

    # 🌐 LANGUAGES FILTER
    selected_languages = request.GET.getlist('languages')
    if selected_languages:
        movies = movies.filter(language__id__in=selected_languages).distinct()

    # 🔽 SORTING
    selected_sort = request.GET.get('sort', 'name')
    if selected_sort == 'rating':
        movies = movies.order_by('-rating')
    else:
        movies = movies.order_by('name')

    # 📊 GENRE COUNTS (IMPORTANT)
    genre_counts = Genre.objects.annotate(
        movie_count=Count('movie')
    )

    # 📊 LANGUAGE COUNTS
    language_counts = Language.objects.annotate(
        movie_count=Count('movie')
    )

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genre_counts': genre_counts,
        'language_counts': language_counts,
        'selected_genres': selected_genres,
        'selected_languages': selected_languages,
        'selected_sort': selected_sort,
        'search_query': search_query,
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