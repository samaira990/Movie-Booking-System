from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from movies.models import Movie, Theater



class MovieNight(models.Model):

    VENUE_CHOICES = [
        ("Cinema", "Cinema"),
        ("Home", "Home"),
    ]

    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_movie_nights"
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_nights"
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name="movie_nights",
        null=True,
        blank=True
    )

    date = models.DateField()

    time = models.TimeField()

    venue_type = models.CharField(
        max_length=20,
        choices=VENUE_CHOICES
    )

    description = models.TextField(
        blank=True,
        help_text="Optional message for your friends."
    )

    invited_users = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name="invited_movie_nights",
    blank=True,
    help_text="Users invited to this movie night."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        """
        If the venue is Cinema, a theater must be selected.
        If the venue is Home, theater should be left empty.
        """

        from django.core.exceptions import ValidationError

        if self.venue_type == "Cinema" and not self.theater:
            raise ValidationError(
                "Please select a theater for a cinema movie night."
            )

        if self.venue_type == "Home" and self.theater:
            raise ValidationError(
                "Home movie nights should not have a theater selected."
            )

    def __str__(self):
        return (
            f"{self.host.username}'s Movie Night - "
            f"{self.movie.name} ({self.date})"
        )


class Invitation(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Declined", "Declined"),
    ]

    movie_night = models.ForeignKey(
        MovieNight,
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="movie_night_invitations"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    invited_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("movie_night", "invited_user")
        ordering = ["-invited_at"]

    def __str__(self):
        return (
            f"{self.invited_user.username} - "
            f"{self.movie_night.movie.name} ({self.status})"
        )