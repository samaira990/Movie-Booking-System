from datetime import timedelta

from django.db import transaction, IntegrityError
from django.utils import timezone

from .models import SeatLock
from movies.models import Booking


def lock_seat(user, show, seat):
    """
    Try to lock a seat for 2 minutes.
    Returns: (success: bool, message: str)
    """

    try:
        with transaction.atomic():

            existing_lock = (
                SeatLock.objects
                .select_for_update()
                .filter(
                    show=show,
                    seat=seat,
                    status="active"
                )
                .first()
            )

            if existing_lock:
                if existing_lock.is_expired():
                    existing_lock.status = "expired"
                    existing_lock.save()
                else:
                    return False, "Seat is already locked by another user"

            SeatLock.objects.create(
                user=user,
                show=show,
                seat=seat,
                expires_at=timezone.now() + timedelta(minutes=2)
            )

            return True, "Seat locked successfully"

    except IntegrityError:
        return False, "Seat already locked"


def create_booking(user, show, seat):
    print("DEBUG: create_booking called")  # TEMP DEBUG

    booking = Booking.objects.create(
        user=user,
        seat=seat,
        movie=show.movie,
        theater=show
    )

    print("DEBUG: booking created ->", booking)

    return booking