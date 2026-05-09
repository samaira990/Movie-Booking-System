from django.urls import path
from .views import lock_seat_view

urlpatterns = [
    path(
        "lock-seat/",
        lock_seat_view,
        name="lock_seat"
    ),
]