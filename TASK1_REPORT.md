# TASK 1 REPORT — Scalable Movie Browsing System with Filtering & Pagination

## Overview

Task 1 focused on building a scalable movie browsing system capable of handling large datasets efficiently while maintaining smooth filtering, searching, sorting, and pagination functionality.

The system was designed to support realistic movie discovery workflows similar to modern movie booking platforms.

---

# Objectives Achieved

## ✅ Large Scale Dataset Support

The movie database was expanded to support large-scale records for scalability testing.

### Implementation

- Migrated the database from Render PostgreSQL to Neon PostgreSQL for better reliability and persistence.
- Generated and inserted 5000+ synthetic movie records.
- Used optimized Django ORM operations for efficient insertion.

### Optimization Used

```python
Movie.objects.bulk_create(movie_list, batch_size=500)