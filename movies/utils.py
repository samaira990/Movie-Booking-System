import io
import base64
import qrcode

from django.core.mail import send_mail
from django.conf import settings


def generate_qr(booking):
    """
    Generates QR code for booking and returns a base64 image string
    usable directly in HTML <img> tag
    """

    # More compact + scanner-friendly format
    data = (
        f"BOOKING_ID:{booking.id}|"
        f"USER:{booking.user.username}|"
        f"MOVIE:{booking.movie.name}|"
        f"THEATER:{booking.theater.name}|"
        f"SEAT:{booking.seat.seat_number}|"
        f"STATUS:{booking.status}"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return "data:image/png;base64," + qr_base64


def send_booking_email(booking):
    """
    Sends real booking confirmation email via SMTP
    """

    # Safety check
    if not booking.user.email:
        return False

    subject = "🎬 Your Movie Ticket is Confirmed!"

    message = (
        f"Hi {booking.user.username},\n\n"
        f"Your booking has been confirmed successfully 🎉\n\n"
        f"Booking Details:\n"
        f"Movie: {booking.movie.name}\n"
        f"Theater: {booking.theater.name}\n"
        f"Seat: {booking.seat.seat_number}\n"
        f"Amount: ₹{booking.amount}\n"
        f"Status: {booking.status}\n\n"
        f"Enjoy your movie 🍿"
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [booking.user.email],
        fail_silently=False
    )

    return True