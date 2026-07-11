from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/notifications", tags=["notifications"])


def simulate_send(channel: models.NotificationChannel) -> bool:
    """
    Stand-in for a real email/SMS/push provider (e.g. SendGrid, Twilio, FCM).
    Always 'succeeds' for this MVP.
    """
    return True


@router.post("/", response_model=schemas.NotificationResponse, status_code=201)
def create_notification(payload: schemas.NotificationCreate, db: Session = Depends(get_db)):
    if payload.payment_id:
        payment = db.query(models.Payment).filter(models.Payment.id == payload.payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Referenced payment not found")

    notification = models.Notification(
        payment_id=payload.payment_id,
        recipient=payload.recipient,
        channel=payload.channel,
        message=payload.message,
        status=models.NotificationStatus.QUEUED,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    sent = simulate_send(notification.channel)
    notification.status = models.NotificationStatus.SENT if sent else models.NotificationStatus.FAILED
    db.commit()
    db.refresh(notification)

    return notification


@router.get("/{notification_id}", response_model=schemas.NotificationResponse)
def get_notification(notification_id: str, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.get("/", response_model=list[schemas.NotificationResponse])
def list_notifications(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Notification).offset(skip).limit(limit).all()
