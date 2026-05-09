from datetime import timedelta

from django.db import transaction, IntegrityError
from django.utils import timezone

from .models import SeatLock


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
                    # remove expired lock
                    existing_lock.delete()
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