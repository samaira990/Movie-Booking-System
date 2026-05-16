import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_booking_confirmation_email(
    user_email,
    movie_name,
    seats,
    show_time,
    booking_id,
    payment_id,
):
    subject = "Booking Confirmed"

    context = {
        "movie_name": movie_name,
        "seats": seats,
        "show_time": show_time,
        "booking_id": booking_id,
        "payment_id": payment_id,
    }

    html_content = render_to_string(
        "emails/booking_confirmation.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your booking is confirmed.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )

    email.attach_alternative(
        html_content,
        "text/html",
    )

    email.send()


def send_booking_email_with_retry(booking, payment):
    """
    Send booking confirmation email.
    Retry once if first attempt fails.
    """

    for attempt in range(2):
        try:
            send_booking_confirmation_email(
                user_email=booking.user.email,
                movie_name=booking.movie.name,
                seats=booking.seat.seat_number,
                show_time=booking.theater.time.strftime("%d %b %Y, %I:%M %p"),
                booking_id=booking.id,
                payment_id=payment.provider_order_id,
            )

            print("Email sent successfully.")
            return

        except Exception as e:
            print(f"Email failed (attempt {attempt+1}): {e}")

            if attempt == 0:
                time.sleep(2)