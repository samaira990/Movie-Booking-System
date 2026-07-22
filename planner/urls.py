from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("create/", views.create_movie_night, name="create_movie_night"),
    path("my/", views.my_movie_nights, name="my_movie_nights"),
    path("<int:pk>/", views.movie_night_detail, name="movie_night_detail"),
    path(
    "movie-preview/<int:movie_id>/",
    views.movie_preview,
    name="movie_preview",
    ),
]