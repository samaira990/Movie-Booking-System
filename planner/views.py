from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import MovieNightForm
from .models import MovieNight
from movies.models import Movie


@login_required
def create_movie_night(request):

    if request.method == "POST":

        # Pass logged-in user to the form
        form = MovieNightForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            movie_night = form.save(commit=False)

            # Automatically assign the logged-in user as the host
            movie_night.host = request.user

            movie_night.save()

            # Save ManyToMany fields (invited users)
            form.save_m2m()

            return redirect("planner:my_movie_nights")

    else:

        form = MovieNightForm(
            user=request.user
        )

    return render(
        request,
        "planner/create_movie_night.html",
        {
            "form": form
        }
    )


@login_required
def my_movie_nights(request):

    movie_nights = (
        MovieNight.objects
        .filter(host=request.user)
        .select_related("movie", "theater")
        .order_by("-created_at")
    )

    return render(
        request,
        "planner/my_movie_nights.html",
        {
            "movie_nights": movie_nights
        }
    )


@login_required
def movie_night_detail(request, pk):

    movie_night = get_object_or_404(
        MovieNight.objects.select_related(
            "movie",
            "host",
            "theater"
        ),
        pk=pk
    )

    return render(
        request,
        "planner/movie_night_detail.html",
        {
            "movie_night": movie_night
        }
    )

def movie_preview(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)

        data = {
            "name": movie.name,
            "rating": str(movie.rating),
            "image": movie.image.url if movie.image else "",
            "genres": ", ".join(
                genre.name for genre in movie.genres.all()
            ),
            "languages": ", ".join(
                language.name for language in movie.languages.all()
            ),
        }

        return JsonResponse(data)

    except Movie.DoesNotExist:
        return JsonResponse({"error": "Movie not found"}, status=404)