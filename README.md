# EventFlow - Hackathon Ticket Booking System

Production-style event ticket booking platform with role-based APIs and a Streamlit frontend.

## 1. Problem Coverage
This project implements the required lifecycle:

`Register -> Browse Events -> Select Seats -> Book -> Confirm/Generate Tickets -> Validate Entry -> Refund/Support`

It includes role separation for:
- `admin`
- `organizer`
- `customer`
- `entry_manager`
- `support`

## 2. Tech Stack
- Backend: FastAPI, Pydantic, JWT auth
- Database: MongoDB (Motor + PyMongo)
- Frontend: Streamlit + Requests
- Auth: `python-jose` + `passlib`

## 3. Core Business Rules Implemented
- Booking is allowed only for `upcoming` events and before event date/time.
- Per-user ticket cap per event is enforced via `max_tickets_per_user`.
- Seat locking/booking lifecycle is enforced (`available -> locked -> booked`).
- Ticket is invalid if:
  - event date has passed
  - ticket is already used
  - ticket is cancelled
- Refund request is allowed only before event date for confirmed bookings.
- On refund approval:
  - booking -> `refunded`
  - payment -> `refunded`
  - seats -> `available`
  - tickets -> `cancelled`
- Support case access is role-based (customer for own cases, support/admin for dashboard/update).

## 4. High-Level Architecture
- `backend/app/main.py` boots FastAPI, middleware, routers, startup/shutdown DB hooks.
- Routers handle role-gated API endpoints.
- Services enforce business logic and rule transitions.
- Models encapsulate Mongo collection operations.
- Utility layer serializes Mongo native values and guards invalid ObjectId usage.
- Frontend consumes backend APIs through role-based Streamlit workspaces.

## 5. Project Structure
```text
Hackathon/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── db.py
│       ├── dependencies.py
│       ├── core/
│       │   ├── constants.py
│       │   ├── roles.py
│       │   └── security.py
│       ├── middleware/
│       │   ├── cors.py
│       │   └── logging_middleware.py
│       ├── models/
│       │   ├── user_models.py
│       │   ├── venue_model.py
│       │   ├── event_model.py
│       │   ├── seat_model.py
│       │   ├── booking_model.py
│       │   ├── ticket_model.py
│       │   ├── refund_model.py
│       │   ├── support_model.py
│       │   ├── entry_log_model.py
│       │   └── order_model.py
│       ├── schemas/
│       │   ├── user_schemas.py
│       │   ├── venue_schema.py
│       │   ├── event_schema.py
│       │   ├── booking_schema.py
│       │   ├── ticket_schema.py
│       │   ├── refund_schema.py
│       │   └── support_schema.py
│       ├── services/
│       │   ├── auth_services.py
│       │   ├── venue_service.py
│       │   ├── event_service.py
│       │   ├── seat_service.py
│       │   ├── booking_service.py
│       │   ├── ticket_service.py
│       │   ├── refund_service.py
│       │   ├── support_service.py
│       │   └── entry_service.py
│       ├── routers/
│       │   ├── auth_router.py
│       │   ├── customer_router.py
│       │   ├── organizer_router.py
│       │   ├── admin_router.py
│       │   ├── support_router.py
│       │   └── entry_router.py
│       └── utils/
│           └── mongo_helpers.py
└── frontend/
    ├── app.py
    ├── requirements.txt
    └── .streamlit/
        └── config.toml
```

## 6. Data Model (Mongo Collections)
- `users`: profile, role, auth flags
- `venues`: venue master
- `events`: event details, pricing, status, limits
- `seats`: seat inventory and lock/book status
- `bookings`: cart/checkout booking record
- `tickets`: generated ticket codes and usage status
- `refunds`: refund lifecycle
- `support_cases`: support tickets and responses
- `entry_logs`: gate validation logs

## 7. API Endpoints by Role

### Auth (`/auth`)
- `POST /auth/register`
- `POST /auth/login`

### Customer (`/customer`)
- `GET /customer/events`
- `GET /customer/events/{event_id}`
- `GET /customer/events/{event_id}/seats`
- `POST /customer/bookings`
- `POST /customer/bookings/{booking_id}/confirm`
- `GET /customer/bookings`
- `GET /customer/bookings/{booking_id}`
- `POST /customer/bookings/{booking_id}/cancel`
- `GET /customer/tickets`
- `GET /customer/tickets/{ticket_id}`
- `POST /customer/refunds`
- `POST /customer/support`
- `GET /customer/support`

### Organizer (`/organizer`)
- `POST /organizer/events`
- `GET /organizer/events`
- `PUT /organizer/events/{event_id}`
- `DELETE /organizer/events/{event_id}`
- `POST /organizer/events/{event_id}/seats`
- `GET /organizer/events/{event_id}/bookings`
- `GET /organizer/events/{event_id}/entries`

### Entry Manager (`/entry`)
- `POST /entry/login`
- `POST /entry/validate`
- `GET /entry/event/{event_id}`
- `GET /entry/ticket/{ticket_id}`

### Support Executive (`/support` + admin refund endpoints)
- `GET /support/admin`
- `PUT /support/admin/{ticket_id}`
- `GET /admin/refunds`
- `PUT /admin/refunds/{refund_id}/approve`
- `PUT /admin/refunds/{refund_id}/reject`

### Admin (`/admin`)
- `GET /admin/users`
- `POST /admin/venues`
- `GET /admin/bookings`
- `GET /admin/support`
- refund actions above

### System
- `GET /health`
- `GET /docs`

## 8. Frontend Screen Mapping (Sprint 3)
The Streamlit UI includes:
- Customer Journey workspace:
  - Event listing page
  - Event detail + seat selection
  - Cart/checkout flow
  - Ticket confirmation view
  - Ticket validation handoff
- Customer workspace:
  - Full customer actions (bookings, tickets, refunds, support)
- Organizer workspace:
  - Event management + seats + event insights
- Entry workspace:
  - Ticket validation + entry logs
- Support workspace:
  - Support dashboard + refund processing
- Admin workspace:
  - Users, bookings, venue creation, support and refund operations

## 9. Setup and Run

## Prerequisites
- Python 3.10+
- MongoDB connection string

## Backend setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:
```env
MONGO_URL="<your-mongodb-uri>"
DATABASE_NAME="auth_db"
SECRET_KEY="supersecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run backend:
```bash
uvicorn app.main:app --reload
```

Backend URLs:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Frontend setup
```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Frontend URL:
- `http://localhost:8501`

## 10. End-to-End Demo Flow (Recommended)
1. Register customer and login.
2. As admin, create venue.
3. As organizer, create event and seats.
4. As customer, browse events and seats.
5. Create booking and confirm booking (ticket generation).
6. View tickets.
7. As entry manager, validate ticket once (allowed), second time (rejected as used).
8. Request refund before event date.
9. As support/admin, approve refund and verify:
   - booking refunded
   - seats available
   - ticket cancelled
10. Create and resolve support case.

## 11. Quality/Robustness Enhancements in Code
- Safe ObjectId parsing in model layer (prevents invalid-ID 500 errors).
- Mongo ObjectId/datetime to JSON serialization helper.
- DB connectivity guard with explicit 503 responses.
- Unique indexes for key collections (`users.email`, `tickets.ticket_code`, `seats(event_id,seat_number)`, `refunds.booking_id`).
- Ownership checks for sensitive operations (ticket/booking/event scope).


