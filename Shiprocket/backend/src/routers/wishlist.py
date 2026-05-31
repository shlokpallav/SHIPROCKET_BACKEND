from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.wishlist import Wishlist

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/add")
def add_to_wishlist(user_id: int, product_id: int, db: Session = Depends(get_db)):
    item = Wishlist(user_id=user_id, product_id=product_id)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Added to wishlist",
        "wishlist_item_id": item.id
    }


@router.get("/{user_id}")
def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return items


@router.delete("/remove")
def remove_from_wishlist(user_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.product_id == product_id
    ).first()

    if not item:
        return {"message": "Item not found in wishlist"}

    db.delete(item)
    db.commit()

    return {"message": "Product removed from wishlist"}
