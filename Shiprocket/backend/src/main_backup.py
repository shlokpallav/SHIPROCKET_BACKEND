from fastapi import FastAPI

from src.database import Base, engine
from src.models import user
from src.routers import shipping, auth, payment, otp

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(shipping.router)
app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(otp.router)


@app.get("/")
def root():
    return {"message": "Shiprocket Backend Running"}