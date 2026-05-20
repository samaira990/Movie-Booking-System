from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)

    release_date = models.DateField(null=True, blank=True)

    trailer_url = models.URLField(
        null=True,
        blank=True
    )

    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    languages = models.ManyToManyField(Language, related_name='movies', blank=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.trailer_url:
            if (
                "youtube.com" not in self.trailer_url
                and "youtu.be" not in self.trailer_url
            ):
                raise ValidationError(
                    {
                        "trailer_url": "Invalid trailer URL. Only YouTube URLs are allowed."
                    }
                )
    @property
    def trailer_embed_url(self):
        if not self.trailer_url:
            return None

        if "youtu.be/" in self.trailer_url:
            video_id = self.trailer_url.split("youtu.be/")[-1].split("?")[0]

        elif "watch?v=" in self.trailer_url:
            video_id = self.trailer_url.split("watch?v=")[-1].split("&")[0]

        else:
            return None

        return f"https://www.youtube.com/embed/{video_id}?rel=0"   
 
class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.movie.name} at {self.time}"


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('theater', 'seat_number')

    def __str__(self):
        return f"{self.seat_number} in {self.theater.name}"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    seat = models.OneToOneField(
        Seat,
        on_delete=models.CASCADE
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=250.00
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Booking by {self.user.username} "
            f"for {self.seat.seat_number} "
            f"at {self.theater.name}"
        )
    

