from fastapi import FastAPI

from database import Base, engine
from routers import payments, notifications

# Create tables on startup (fine for MVP/dev; use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment & Notification Microservice",
    description="A FastAPI microservice that processes payments and dispatches notifications.",
    version="1.0.0",
)

app.include_router(payments.router)
app.include_router(notifications.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "payment-notification-service"}
