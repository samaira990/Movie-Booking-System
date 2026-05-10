from django.urls import path
from .views import lock_seat_view
from .views import lock_seat_view, release_seat_view

urlpatterns = [
    path("lock-seat/", lock_seat_view, name="lock_seat"),
    path("release-seat/", release_seat_view, name="release_seat"),
]