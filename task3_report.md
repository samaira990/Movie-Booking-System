# TASK 3 REPORT — Async Booking Confirmation Email Notifications

## Overview

Implemented an automated email notification system that sends booking confirmation emails immediately after successful payment verification.

The system sends emails asynchronously in the background to avoid delaying API responses and includes retry logic for reliability.

This ensures users receive instant booking confirmation while keeping the payment webhook fast and efficient.

---

## Objectives

The main goals of this task were:

- Send booking confirmation email only after successful payment
- Automatically trigger email after Stripe webhook verification
- Prevent duplicate email notifications
- Keep payment API response fast
- Send emails asynchronously in the background
- Retry email sending if a temporary failure occurs

---

## System Flow

Seat selected  
↓  
Booking created (pending)  
↓  
Stripe payment initiated  
↓  
Stripe webhook received  
↓  
Payment verified successfully  
↓  
Payment marked as success  
↓  
Booking status updated to confirmed  
↓  
Background email thread started  
↓  
Webhook returns immediately (no delay)  
↓  
Booking confirmation email sent

---

## 1. Notifications App Setup

Created a dedicated Django app for handling notification-related logic:

```bash
python manage.py startapp notifications
```

### Purpose

- Separate email logic from payment logic
- Keep project structure modular
- Improve maintainability
- Make notification utilities reusable

---

## 2. Email Backend Configuration

Updated `settings.py` with:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@bookmyshowclone.com"
```

### Why console backend?

For local development and testing:

- Avoids SMTP setup complexity
- No email provider authentication needed
- Safe debugging
- Email content prints directly in terminal

This allows verification of email formatting and dynamic content before integrating a real email provider.

---

## 3. Email Template Creation

Created template file:

```text
templates/emails/booking_confirmation.html
```

### Template Contents

The booking confirmation email displays:

- Movie name
- Seat number
- Show time
- Booking ID
- Payment ID

### HTML Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Booking Confirmed</title>
</head>
<body>
    <h2>🎉 Booking Confirmed!</h2>

    <p>Your movie ticket has been successfully booked.</p>

    <hr>

    <p><strong>Movie:</strong> {{ movie_name }}</p>
    <p><strong>Seats:</strong> {{ seats }}</p>
    <p><strong>Show Time:</strong> {{ show_time }}</p>
    <p><strong>Booking ID:</strong> {{ booking_id }}</p>
    <p><strong>Payment ID:</strong> {{ payment_id }}</p>

    <hr>

    <p>Thank you for booking with us.</p>
</body>
</html>
```

---

## 4. Email Utility Implementation

Created file:

```text
notifications/utils.py
```

Implemented:

```python
send_booking_confirmation_email()
```

### Responsibilities

This function:

- Renders HTML email template
- Generates plain-text fallback
- Creates multipart email
- Sends booking confirmation email

### Technologies Used

- `EmailMultiAlternatives`
- `render_to_string`
- Django settings configuration

---

## 5. Retry Logic Implementation

Implemented helper:

```python
send_booking_email_with_retry()
```

### Retry Strategy

1. Attempt email send
2. If sending fails:
   - Print error message
   - Wait 2 seconds
   - Retry once

### Flow

```text
Try email
   ↓
Success → Stop
   ↓
Failure
   ↓
Wait 2 seconds
   ↓
Retry once
```

### Purpose

Improves reliability in case of:

- Temporary network issues
- SMTP service interruptions
- Rendering failures

---

## 6. Asynchronous Email Sending

Used Python threading for background email execution:

```python
threading.Thread(
    target=send_booking_email_with_retry,
    args=(booking, payment),
).start()
```

### Why async?

Without threading:

```text
Webhook waits until email finishes sending
```

Possible problems:

- Slow API response
- Payment confirmation delay
- Poor user experience

With threading:

```text
Webhook returns immediately
Email sends in background
```

### Benefits

- Faster webhook response
- Non-blocking backend
- Better scalability
- Improved user experience

---

## 7. Stripe Webhook Integration

Updated:

```text
payments/views.py
```

### Added imports

```python
import threading
from notifications.utils import send_booking_email_with_retry
```

### Email Trigger After Successful Payment

Added inside Stripe success webhook:

```python
if event_type == "payment_intent.succeeded":

    if payment.status == "success":
        return HttpResponse(status=200)

    payment.status = "success"
    payment.save()

    booking = payment.booking
    booking.status = "confirmed"
    booking.save()

    threading.Thread(
        target=send_booking_email_with_retry,
        args=(booking, payment),
    ).start()
```

---

## 8. Idempotency Protection

Stripe can resend webhook events.

To prevent duplicate processing:

```python
if payment.status == "success":
    return HttpResponse(status=200)
```

### Benefits

- Prevents duplicate booking confirmation
- Prevents duplicate emails
- Makes webhook safe for repeated events

---

## 9. Stripe CLI Setup for Local Webhook Testing

Initially, Stripe webhook events were not reaching the local Django server.

### Installed Stripe CLI

```bash
winget install Stripe.StripeCLI
```

### Verified Installation

```bash
stripe version
```

### Logged into Stripe

```bash
stripe login
```

### Started Webhook Forwarding

```bash
stripe listen --forward-to localhost:8000/payments/webhook/
```

### Received Webhook Secret

```text
whsec_xxxxxxxxxxxxxxxxx
```

Updated `.env`:

```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxx
```

Restarted Django server afterward.

---

## 10. Debugging and Fixes

### Issue 1: Template Not Found

#### Error

```text
TemplateDoesNotExist: emails/booking_confirmation.html
```

#### Cause

Template file was missing or placed incorrectly.

#### Fix

Created:

```text
templates/emails/booking_confirmation.html
```

---

### Issue 2: Stripe Webhook Not Updating Payments

#### Symptom

Payments remained in:

```text
Pending
```

#### Cause

Stripe CLI webhook forwarding was not configured.

#### Fix

Installed Stripe CLI and forwarded webhook events locally.

---

### Issue 3: Incorrect Booking Model Field Names

#### Error

```text
'Booking' object has no attribute 'show'
```

#### Cause

Email utility used incorrect field references.

Incorrect fields:

```python
booking.show.movie.title
booking.seats.all()
booking.show.show_time
payment.payment_id
```

Corrected to:

```python
booking.movie.name
booking.seat.seat_number
booking.theater.time
payment.provider_order_id
```

---

## 11. Testing Performed

### Test 1: Manual Email Utility Test

Executed in Django shell:

```python
from notifications.utils import send_booking_confirmation_email
send_booking_confirmation_email(...)
```

### Result

- Email rendered successfully
- HTML displayed correctly in terminal

---

### Test 2: Full Payment Flow

Tested complete booking flow:

```text
Create booking
→ Start Stripe payment
→ Complete payment
→ Stripe webhook triggered
→ Payment marked success
→ Booking confirmed
→ Email sent automatically
```

Observed:

```text
POST /payments/webhook/ HTTP/1.1 200
```

And:

```text
Email sent successfully.
```

---

### Test 3: Async Verification

Observed:

```text
POST /payments/webhook/ 200
Email sent successfully.
```

Confirmed:

- Webhook returned immediately
- Email executed afterward
- No blocking occurred

---

### Test 4: Retry Verification

Simulated email failure.

Observed:

```text
Email failed (attempt 1)
Email sent successfully.
```

Confirmed retry mechanism works.

---

## Final Results

Successfully implemented a robust asynchronous booking confirmation email notification system.

### Features Completed

- Automatic booking confirmation emails
- HTML-formatted email template
- Stripe webhook integration
- Async background email sending
- Retry on temporary failures
- Duplicate-safe webhook handling
- Fast API response
- Successful local testing

---

## Completion Checklist

✅ Booking confirmed after successful payment  
✅ Payment status updated correctly  
✅ Email triggered automatically  
✅ Email sent asynchronously  
✅ No API delay observed  
✅ Retry mechanism implemented  
✅ Duplicate email prevention enabled  
✅ HTML email rendered successfully  

---

## Conclusion

Task 3 completed successfully.

The movie booking system now provides automatic, reliable, and asynchronous booking confirmation emails immediately after successful payment, improving user experience while maintaining fast backend performance.