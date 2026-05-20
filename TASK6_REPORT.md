# TASK 6 REPORT — Advanced Admin Analytics Dashboard

## Overview

Built a secure admin analytics dashboard for the movie booking system.

The dashboard provides real-time aggregated insights into platform activity using optimized database queries, caching, and role-based access control.

---

## Metrics Implemented

### 1. Total Revenue

Implemented daily, weekly, and monthly revenue aggregation using Django ORM database functions.

Techniques used:
- `Sum()`
- `TruncDate()`
- `TruncWeek()`
- `TruncMonth()`

Revenue is calculated only from confirmed bookings.

### Current Revenue Results

**Daily Revenue**
- 2026-05-16 → ₹500.00
- 2026-05-14 → ₹250.00

**Weekly Revenue**
- Week starting 2026-05-11 → ₹750.00

**Monthly Revenue**
- May 2026 → ₹750.00

---

### 2. Most Popular Movies

Calculated most-booked movies based on confirmed booking counts.

Technique used:
- `Count()`
- grouped by `movie__name`

### Current Results
- Avengers: Endgame → 1 booking
- Movie 11 → 1 booking
- Movie 21 → 1 booking

---

### 3. Busiest Theaters

Calculated busiest theaters using confirmed booking counts per theater.

Note:
Exact seat occupancy percentage could not be computed because theater total capacity is not stored in the current schema. Booking count per theater was used as an occupancy approximation.

### Current Results
- Theater 1 → 1 booking
- Theater 3 → 1 booking
- Theater 4 → 1 booking

---

### 4. Peak Booking Hours

Identified busiest booking times by extracting booking hour.

Technique used:
- `ExtractHour()`
- `Count()`

### Current Results
- 17:00 → 2 bookings
- 21:00 → 1 booking
- 00:00 → 1 booking
- 18:00 → 1 booking
- 07:00 → 1 booking

Peak booking hour:
- **17:00 (5 PM)**

---

### 5. Cancellation Rate

Computed cancellation percentage using:

`cancelled bookings / total bookings × 100`

### Current Result
- **16.67%**

---

## Query Optimization

All analytics were implemented using database-side aggregation.

Optimizations:
- No full dataset loading into Python
- No manual loops
- Efficient ORM aggregation queries
- `select_related()` for related objects

---

## Indexing Strategy

Added database indexes on frequently queried fields:

- `Booking.status`
- `Booking.booked_at`

Foreign key indexes already provided automatically by Django:

- `Booking.movie`
- `Booking.theater`

Migration applied successfully.

---

## Caching

Implemented local memory caching using Django cache framework.

Configuration:
- `LocMemCache`
- Cache timeout: **300 seconds**

Repeated dashboard requests are served from cache for faster response.

---

## Security

Dashboard access is restricted to admin/staff users only.

Protection used:
- `@staff_member_required`

Unauthorized users are redirected to login.

Additional security:
- Django session authentication
- Password hashing (default Django auth system)

---

## Analytics Endpoint

Dashboard URL:

`/analytics/dashboard/`

Returns JSON analytics response containing:
- Revenue analytics
- Popular movies
- Busiest theaters
- Peak booking hours
- Cancellation rate

---

## Admin Credentials

[Add your admin username and password here if required by your instructor]

Example:

Username: admin  
Password: ********

---

## Conclusion

Successfully built a secure and optimized admin analytics dashboard with:

- Real-time analytics
- Aggregation optimization
- Indexed database queries
- Cached responses
- Admin-only secure access

Task 6 completed successfully.