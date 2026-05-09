from django.http import JsonResponse
from .services import lock_seat
from movies.models import Theater, Seat


def lock_seat_view(request):
    user = request.user

    # Require login
    if not user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Login required"
        })

    # Get URL parameters
    show_id = request.GET.get("show_id")
    seat_id = request.GET.get("seat_id")

    try:
        # Fetch theater and seat
        show = Theater.objects.get(id=show_id)
        seat = Seat.objects.get(id=seat_id)

    except Theater.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid theater"
        })

    except Seat.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid seat"
        })

    # Try locking seat
    success, message = lock_seat(
        user,
        show,
        seat
    )

    return JsonResponse({
        "success": success,
        "message": message
    })