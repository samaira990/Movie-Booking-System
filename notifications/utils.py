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