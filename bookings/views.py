import logging

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from movies.models import Theater, Seat
from .models import SeatLock
from .services import lock_seat, create_booking

logger = logging.getLogger(__name__)


# ---------------------------
# LOCK SEAT VIEW
# ---------------------------
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

    # Validate input
    if not show_id or not seat_id:
        return JsonResponse({
            "success": False,
            "message": "Missing show_id or seat_id"
        })

    try:
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

    # Lock seat
    success, message = lock_seat(user, show, seat)

    # Create booking only if lock is successful
    if success:
        create_booking(user, show, seat)
        logger.info("Booking created for user %s", user.username)

    return JsonResponse({
        "success": success,
        "message": message
    })


# ---------------------------
# RELEASE SEAT VIEW
# ---------------------------
def release_seat_view(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Login required"
        })

    show_id = request.GET.get("show_id")
    seat_id = request.GET.get("seat_id")

    if not show_id or not seat_id:
        return JsonResponse({
            "success": False,
            "message": "Missing show_id or seat_id"
        })

    try:
        lock = SeatLock.objects.get(
            user=user,
            show_id=show_id,
            seat_id=seat_id,
            status="active"
        )

        lock.status = "released"
        lock.save()

        logger.info(
            "Seat released by user %s (show_id=%s, seat_id=%s)",
            user.username,
            show_id,
            seat_id
        )

        return JsonResponse({
            "success": True,
            "message": "Seat released successfully"
        })

    except SeatLock.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "No active lock found"
        })