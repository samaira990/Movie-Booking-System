from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, ExtractHour

from movies.models import Booking


def get_revenue_analytics():
    """
    Revenue from confirmed bookings only
    grouped by day / week / month.
    """

    confirmed = Booking.objects.filter(
        status="confirmed"
    )

    daily = (
        confirmed
        .annotate(day=TruncDate("booked_at"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("-day")
    )

    weekly = (
        confirmed
        .annotate(week=TruncWeek("booked_at"))
        .values("week")
        .annotate(total=Sum("amount"))
        .order_by("-week")
    )

    monthly = (
        confirmed
        .annotate(month=TruncMonth("booked_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("-month")
    )

    return {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
    }


def get_popular_movies():
    """
    Movies with highest booking counts.
    """

    return (
        Booking.objects
        .filter(status="confirmed")
        .values("movie__name")
        .annotate(total_bookings=Count("id"))
        .order_by("-total_bookings")
    )


def get_peak_booking_hours():
    """
    Which booking hours are busiest.
    """

    return (
        Booking.objects
        .annotate(hour=ExtractHour("booked_at"))
        .values("hour")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_cancellation_rate():
    """
    Percentage of cancelled bookings.
    """

    total = Booking.objects.count()

    cancelled = Booking.objects.filter(
        status="cancelled"
    ).count()

    if total == 0:
        return 0

    return round(
        (cancelled / total) * 100,
        2
    )


def get_busiest_theaters():
    """
    Theaters with most confirmed bookings.
    Approximation of occupancy.
    """

    return (
        Booking.objects
        .filter(status="confirmed")
        .values("theater__name")
        .annotate(total_bookings=Count("id"))
        .order_by("-total_bookings")
    )