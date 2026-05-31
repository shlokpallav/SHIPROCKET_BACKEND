from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.product import Product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/add")
def add_product(
    name: str,
    price: float,
    description: str = None,
    image_url: str = None,
    db: Session = Depends(get_db)
):
    product = Product(
        name=name,
        price=price,
        description=description,
        image_url=image_url
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "message": "Product added successfully",
        "product_id": product.id,
        "product": product
    }


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product not found"}

    return product
