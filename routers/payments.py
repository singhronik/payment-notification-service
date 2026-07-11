import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/payments", tags=["payments"])


def simulate_payment_gateway() -> bool:
    """
    Stand-in for a real payment gateway (e.g. Stripe/Razorpay).
    Returns True (success) ~85% of the time.
    """
    return random.random() < 0.85


@router.post("/", response_model=schemas.PaymentResponse, status_code=201)
def create_payment(payload: schemas.PaymentCreate, db: Session = Depends(get_db)):
    payment = models.Payment(
        order_reference=payload.order_reference,
        amount=payload.amount,
        currency=payload.currency,
        status=models.PaymentStatus.PENDING,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Simulate processing synchronously for this MVP.
    success = simulate_payment_gateway()
    payment.status = models.PaymentStatus.SUCCESS if success else models.PaymentStatus.FAILED
    db.commit()
    db.refresh(payment)

    return payment


@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/", response_model=list[schemas.PaymentResponse])
def list_payments(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Payment).offset(skip).limit(limit).all()


@router.post("/{payment_id}/refund", response_model=schemas.PaymentResponse)
def refund_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != models.PaymentStatus.SUCCESS:
        raise HTTPException(status_code=400, detail="Only successful payments can be refunded")
    payment.status = models.PaymentStatus.REFUNDED
    db.commit()
    db.refresh(payment)
    return payment
