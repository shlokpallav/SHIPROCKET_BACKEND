import razorpay
import hmac
import hashlib
import os

from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_SECRET,
    )
)


def create_razorpay_order(amount: int):

    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
    }

    order = client.order.create(data=order_data)

    return order


def verify_payment_signature(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):

    generated_signature = hmac.new(
        bytes(RAZORPAY_SECRET, "utf-8"),
        bytes(
            f"{razorpay_order_id}|{razorpay_payment_id}",
            "utf-8"
        ),
        hashlib.sha256,
    ).hexdigest()

    return generated_signature == razorpay_signature