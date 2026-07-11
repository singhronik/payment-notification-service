# Payment & Notification Microservice

A FastAPI microservice that simulates payment processing and dispatches notifications (email/SMS/push) — designed to plug into the companion Order Management System.

## Features

- Create and process payments (simulated gateway, easy to swap for Stripe/Razorpay)
- Refund flow for successful payments
- Multi-channel notifications (email, SMS, push) tied to a payment or standalone
- Auto-generated interactive API docs (Swagger UI + ReDoc)
- SQLite by default, swappable via `DATABASE_URL` env var

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- Uvicorn (ASGI server)

## Project Structure

```
payment-notification-service/
├── main.py               # FastAPI app + router registration
├── database.py           # SQLAlchemy engine/session setup
├── models.py              # ORM models: Payment, Notification
├── schemas.py             # Pydantic request/response schemas
├── routers/
│   ├── payments.py         # /payments endpoints
│   └── notifications.py    # /notifications endpoints
└── requirements.txt
```

## Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/payment-notification-service.git
cd payment-notification-service

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive Swagger docs.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/` | Health check |
| POST | `/payments/` | Create and process a payment |
| GET | `/payments/` | List payments |
| GET | `/payments/{id}` | Get a single payment |
| POST | `/payments/{id}/refund` | Refund a successful payment |
| POST | `/notifications/` | Queue and send a notification |
| GET | `/notifications/` | List notifications |
| GET | `/notifications/{id}` | Get a single notification |

## Example: Create a Payment

```bash
curl -X POST http://127.0.0.1:8000/payments/ \
  -H "Content-Type: application/json" \
  -d '{"order_reference": "ORDER-1001", "amount": 49.99, "currency": "USD"}'
```

## Example: Send a Notification

```bash
curl -X POST http://127.0.0.1:8000/notifications/ \
  -H "Content-Type: application/json" \
  -d '{"recipient": "user@example.com", "channel": "EMAIL", "message": "Your payment was successful!"}'
```

## Roadmap / Possible Extensions

- Real payment gateway integration (Stripe/Razorpay)
- Real notification providers (SendGrid for email, Twilio for SMS, FCM for push)
- Async background processing with Celery or FastAPI BackgroundTasks
- JWT-based service-to-service authentication
- Dockerfile + docker-compose
- Alembic migrations instead of `create_all`

## License

MIT
