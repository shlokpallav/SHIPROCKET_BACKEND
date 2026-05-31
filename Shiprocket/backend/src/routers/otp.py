import random
import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, Form

router = APIRouter()

otp_store = {}

EMAIL_ADDRESS = "shlokpallav@gmail.com"
EMAIL_PASSWORD = "tgnc nuav lqvs ncux"


def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "Your Login OTP"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@router.post("/send-otp")
def send_otp(email: str = Form(...)):
    otp = str(random.randint(100000, 999999))

    otp_store[email] = otp

    send_otp_email(email, otp)

    return {
        "success": True,
        "message": "OTP sent successfully"
    }


@router.post("/verify-otp")
def verify_otp(email: str = Form(...), otp: str = Form(...)):
    if email in otp_store and otp_store[email] == otp:
        del otp_store[email]

        return {
            "success": True,
            "message": "Login successful"
        }

    return {
        "success": False,
        "message": "Invalid OTP"
    }