from django.contrib import admin
from .models import Movie, Theater, Seat, Booking, Genre, Language

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'release_date']
    list_filter = ['genres', 'languages', 'release_date']
    search_fields = ['name', 'cast', 'description']
    filter_horizontal = ['genres', 'languages']
    list_per_page = 20  


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']
    list_filter = ['movie', 'time']
    search_fields = ['name', 'movie__name']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']
    list_filter = ['is_booked', 'theater']
    search_fields = ['seat_number', 'theater__name']
    list_per_page = 50

    actions = ['mark_as_booked', 'mark_as_available']

    def mark_as_booked(self, request, queryset):
        updated = queryset.filter(is_booked=False).update(is_booked=True)
        self.message_user(request, f"{updated} seats marked as booked")
    mark_as_booked.short_description = "Mark selected seats as Booked"

    def mark_as_available(self, request, queryset):
        updated = queryset.filter(is_booked=True).update(is_booked=False)
        self.message_user(request, f"{updated} seats marked as available")
    mark_as_available.short_description = "Mark selected seats as Available"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'theater', 'seat', 'booked_at']
    list_filter = ['movie', 'theater', 'booked_at']
    search_fields = ['user__username', 'movie__name']
    date_hierarchy = 'booked_at'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_count']

    def movie_count(self, obj):
        return obj.movies.count()

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_count']

    def movie_count(self, obj):
        return obj.movies.count()
