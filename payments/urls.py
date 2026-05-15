from django.urls import path
from .views import start_payment, stripe_webhook

urlpatterns = [
    path("start/<int:booking_id>/", start_payment, name="start_payment"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
]