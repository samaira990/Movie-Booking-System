from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Theatre(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Screen(models.Model):
    theatre = models.ForeignKey(
        Theatre,
        on_delete=models.CASCADE,
        related_name="screens"
    )
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.theatre.name} - {self.name}"


class Seat(models.Model):

    SEAT_TYPES = (
        ("Regular", "Regular"),
        ("Premium", "Premium"),
        ("Recliner", "Recliner"),
    )

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name="seats"
    )

    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(
        max_length=20,
        choices=SEAT_TYPES,
        default="Regular"
    )

    def __str__(self):
        return f"{self.screen.name} - {self.seat_number}"


class Show(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name="shows"
    )

    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.show_time}"


class Booking(models.Model):

    BOOKING_STATUS = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="movie_bookings"
    )

    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="movie_bookings"
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="Pending"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.show}"


class BookedSeat(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booked_seats"
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.booking} - {self.seat.seat_number}"
