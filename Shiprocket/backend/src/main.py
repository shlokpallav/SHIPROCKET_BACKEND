from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.models import (
    user,
    product,
    cart,
    wishlist,
    order,
    order_item,
    appointment
)

from src.routers import (
    shipping,
    auth,
    payment,
    otp,
    cart,
    wishlist,
    product,
    order,
    calendar,
    appointment
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shiprocket Backend",
    description="Backend API with products, orders, payments, shipping, Google Calendar and appointments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shipping.router)
app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(otp.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(order.router)
app.include_router(calendar.router)
app.include_router(appointment.router)


@app.get("/")
def root():
    return {"message": "Shiprocket Backend Running"}