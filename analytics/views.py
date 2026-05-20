from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache

from .services import (
    get_revenue_analytics,
    get_popular_movies,
    get_peak_booking_hours,
    get_cancellation_rate,
    get_busiest_theaters,
)


@staff_member_required
def analytics_dashboard(request):
    """
    Admin-only analytics dashboard.
    Cached for 5 minutes.
    """

    cached_data = cache.get("dashboard_data")

    if cached_data:
        return JsonResponse(cached_data)

    revenue = get_revenue_analytics()

    data = {
        "daily_revenue": list(revenue["daily"]),
        "weekly_revenue": list(revenue["weekly"]),
        "monthly_revenue": list(revenue["monthly"]),
        "top_movies": list(get_popular_movies()),
        "busy_theatres": list(get_busiest_theaters()),
        "peak_hours": list(get_peak_booking_hours()),
        "cancellation_rate": get_cancellation_rate(),
    }

    cache.set(
        "dashboard_data",
        data,
        timeout=300
    )

    return JsonResponse(data)