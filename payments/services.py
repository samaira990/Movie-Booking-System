import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_order(booking):
    """
    Create Stripe PaymentIntent + save Payment row
    """

    amount_paise = int(booking.amount * 100)

    intent = stripe.PaymentIntent.create(
        amount=amount_paise,
        currency="inr",
        metadata={
            "booking_id": booking.id
        }
    )

    payment = Payment.objects.create(
        booking=booking,
        provider_order_id=intent.id,
        amount=booking.amount,
        status="pending",
    )

    return {
        "payment": payment,
        "payment_intent_id": intent.id,
        "client_secret": intent.client_secret,
    }