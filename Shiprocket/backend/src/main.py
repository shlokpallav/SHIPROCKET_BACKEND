from fastapi import FastAPI

from src.database import Base, engine
from src.models import user, product, cart, wishlist, order, order_item
from src.routers import shipping, auth, payment, otp, cart, wishlist, product, order

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(shipping.router)
app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(otp.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"message": "Shiprocket Backend Running"}
