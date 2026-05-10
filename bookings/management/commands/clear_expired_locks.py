from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import SeatLock


class Command(BaseCommand):
    help = "Clear expired seat locks"

    def handle(self, *args, **kwargs):
        expired_locks = SeatLock.objects.filter(
            status="active",
            expires_at__lt=timezone.now()
        )

        count = expired_locks.update(
            status="expired"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} expired locks cleared"
            )
        )