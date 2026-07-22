from django.contrib import admin
from .models import MovieNight, Invitation


@admin.register(MovieNight)
class MovieNightAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "host",
        "venue_type",
        "theater",
        "date",
        "time",
        "created_at",
    )

    list_filter = (
        "venue_type",
        "date",
    )

    search_fields = (
        "movie__name",
        "host__username",
    )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "movie_night",
        "invited_user",
        "status",
        "invited_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "invited_user__username",
        "movie_night__movie__name",
    )