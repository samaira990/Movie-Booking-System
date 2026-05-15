from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

from movies.models import Booking
from .models import Payment
from .services import create_payment_order

stripe.api_key = settings.STRIPE_SECRET_KEY


def start_payment(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    result = create_payment_order(booking)

    return render(
        request,
        "payments/checkout.html",
        {
            "client_secret": result["client_secret"],
            "amount": booking.amount,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        }
    )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]

        provider_order_id = payment_intent["id"]

        try:
            payment = Payment.objects.get(
                provider_order_id=provider_order_id
            )

            # IDEMPOTENCY CHECK
            if payment.status == "success":
                return HttpResponse(status=200)

            # First-time success processing
            payment.status = "success"
            payment.save()

            booking = payment.booking
            booking.status = "confirmed"
            booking.save()

        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)