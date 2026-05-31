from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.cart import Cart
from src.models.product import Product
from src.models.order import Order
from src.models.order_item import OrderItem
from src.services.razorpay_service import create_razorpay_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create")
def create_order(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        return {"message": "Cart is empty"}

    total_amount = 0

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total_amount += product.price * item.quantity

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="payment_pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            )
            db.add(order_item)

    db.commit()

    razorpay_order = create_razorpay_order(int(total_amount * 100))

    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "total_amount": total_amount,
        "payment_status": "payment_pending",
        "razorpay_order": razorpay_order
    }


@router.get("/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders
