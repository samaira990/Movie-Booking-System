from django.db import models
from django.conf import settings
from django.utils import timezone

from movies.models import Theater, Seat


class SeatLock(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("released", "Released"),
        ("expired", "Expired"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    show = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.seat} - {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["show"]),
            models.Index(fields=["expires_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "seat"],
                name="unique_show_seat_lock"
            )
        ]