from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.order import Order

from src.services.razorpay_service import (
    create_razorpay_order,
    verify_payment_signature
)

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


class OrderRequest(BaseModel):
    amount: int


class VerifyRequest(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


@router.post("/create-order")
def create_payment_order(data: OrderRequest):
    order = create_razorpay_order(data.amount)

    return {
        "success": True,
        "order": order
    }


@router.post("/verify-payment")
def verify_payment(data: VerifyRequest, db: Session = Depends(get_db)):
    is_valid = verify_payment_signature(
        data.razorpay_order_id,
        data.razorpay_payment_id,
        data.razorpay_signature
    )

    if not is_valid:
        return {
            "success": False,
            "message": "Payment verification failed"
        }

    order = db.query(Order).filter(Order.id == data.order_id).first()

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    order.status = "paid"
    db.commit()
    db.refresh(order)

    return {
        "success": True,
        "message": "Payment verified successfully",
        "order_id": order.id,
        "order_status": order.status
    }
