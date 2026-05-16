# TASK 4 REPORT — Secure Payment Processing

## Overview

Implemented secure payment processing for the movie booking system using Stripe.

The system ensures that bookings are confirmed only after successful backend payment verification.

---

## Payment Lifecycle

Seat lock  
↓  
Booking created (pending)  
↓  
Stripe payment order created  
↓  
User payment attempt  
↓  
Stripe webhook sent to backend  
↓  
Webhook signature verification  
↓  
Payment status updated  
↓  
Booking confirmed on successful payment

---

## Security Measures

### 1. Server-side payment verification

Frontend payment success responses are never trusted directly.

The backend verifies Stripe webhook events before updating any booking or payment records.

---

### 2. Webhook signature verification

Stripe webhook signatures are validated using:

```python
stripe.Webhook.construct_event(...)