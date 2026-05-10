# Task 5 Report

## 1. Overview

Implemented a concurrency-safe temporary
seat reservation system with 2-minute locks
before payment completion.

The system prevents multiple users from
booking the same seat simultaneously and
automatically releases expired reservations.

---

## 2. Race condition prevention

Race conditions are prevented using
transaction.atomic() and select_for_update(),
which apply row-level locking.

When one request locks a seat,
other simultaneous requests must wait
until the transaction finishes.

This guarantees safe concurrent booking.

---

## 3. Database protection

A UniqueConstraint ensures that only
one active lock can exist per seat/show.

This provides an additional safety layer
at the database level against duplicate locks.

---

## 4. Auto timeout

Expired seat locks are automatically released
using the clear_expired_locks management command.

This command identifies active locks whose
expiration time has passed and marks them
as expired.

---

## 5. Edge cases handled

Handled:
- duplicate requests
- simultaneous booking attempts
- browser close
- network interruption
- timeout expiry
- manual lock release

---

## 6. Consistency model

Strong consistency:
a seat can only have one active reservation
at any moment.