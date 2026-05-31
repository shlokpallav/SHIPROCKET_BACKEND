from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.cart import Cart

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(user_id: int, product_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Added to cart",
        "cart_item_id": item.id
    }


@router.get("/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return items


@router.put("/update")
def update_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not item:
        return {"message": "Item not found in cart"}

    item.quantity = quantity
    db.commit()
    db.refresh(item)

    return {
        "message": "Cart updated",
        "cart_item_id": item.id,
        "quantity": item.quantity
    }


@router.delete("/remove")
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not item:
        return {"message": "Item not found in cart"}

    db.delete(item)
    db.commit()

    return {"message": "Product removed from cart"}
