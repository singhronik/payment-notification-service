from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from models import PaymentStatus, NotificationChannel, NotificationStatus


# ---------- Payment schemas ----------

class PaymentCreate(BaseModel):
    order_reference: str = Field(..., examples=["ORDER-1001"])
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    order_reference: str
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime


# ---------- Notification schemas ----------

class NotificationCreate(BaseModel):
    recipient: str = Field(..., examples=["user@example.com"])
    channel: NotificationChannel = NotificationChannel.EMAIL
    message: str
    payment_id: Optional[str] = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    payment_id: Optional[str]
    recipient: str
    channel: NotificationChannel
    message: str
    status: NotificationStatus
    created_at: datetime
