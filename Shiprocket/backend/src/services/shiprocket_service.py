import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHIPROCKET_EMAIL = os.getenv("SHIPROCKET_EMAIL")
SHIPROCKET_PASSWORD = os.getenv("SHIPROCKET_PASSWORD")

BASE_URL = "https://apiv2.shiprocket.in/v1/external"


def shiprocket_login():
    url = f"{BASE_URL}/auth/login"

    payload = {
        "email": SHIPROCKET_EMAIL,
        "password": SHIPROCKET_PASSWORD
    }

    try:
        response = requests.post(url=url, json=payload, timeout=20)
        print("LOGIN STATUS:", response.status_code)
        print("LOGIN RESPONSE:", response.text)
        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Shiprocket login failed",
            "details": str(e)
        }


def get_token():
    token_data = shiprocket_login()
    token = token_data.get("token")

    if not token:
        return None, {
            "success": False,
            "error": "Token not generated",
            "shiprocket_response": token_data
        }

    return token, None


def check_serviceability(pickup_pincode, delivery_pincode, weight, cod):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/courier/serviceability/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "pickup_postcode": pickup_pincode,
        "delivery_postcode": delivery_pincode,
        "weight": weight,
        "cod": cod
    }

    try:
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            timeout=20
        )

        print("SERVICEABILITY STATUS:", response.status_code)
        print("SERVICEABILITY RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Serviceability check failed",
            "details": str(e)
        }


def calculate_shipping_cost(pickup_pincode, delivery_pincode, weight, cod):
    return check_serviceability(
        pickup_pincode,
        delivery_pincode,
        weight,
        cod
    )


def create_order(order_data):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/orders/create/adhoc"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=order_data,
            timeout=20
        )

        print("CREATE ORDER STATUS:", response.status_code)
        print("CREATE ORDER RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Order creation failed",
            "details": str(e)
        }


def track_shipment(awb_code):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/courier/track/awb/{awb_code}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=20
        )

        print("TRACK STATUS:", response.status_code)
        print("TRACK RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Tracking failed",
            "details": str(e)
        }


def generate_label(shipment_id):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/courier/generate/label"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "shipment_id": [shipment_id]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("LABEL STATUS:", response.status_code)
        print("LABEL RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Label generation failed",
            "details": str(e)
        }


def create_pickup_request(shipment_id):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/courier/generate/pickup"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "shipment_id": [shipment_id]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("PICKUP STATUS:", response.status_code)
        print("PICKUP RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Pickup request failed",
            "details": str(e)
        }


def cancel_shipment(awb_code):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/orders/cancel/shipment/awbs"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "awbs": [awb_code]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("CANCEL STATUS:", response.status_code)
        print("CANCEL RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Shipment cancellation failed",
            "details": str(e)
        }


def update_shipment(shipment_id, update_data):
    token, error = get_token()
    if error:
        return error

    url = f"{BASE_URL}/orders/update/adhoc"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    update_data["shipment_id"] = shipment_id

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=update_data,
            timeout=20
        )

        print("UPDATE STATUS:", response.status_code)
        print("UPDATE RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Shipment update failed",
            "details": str(e)
        }
def download_document(shipment_id):

    token, error = get_token()

    if error:
        return error

    url = f"{BASE_URL}/courier/download/invoice"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "shipment_id": shipment_id
    }

    try:
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            timeout=20
        )

        print("DOCUMENT STATUS:", response.status_code)
        print("DOCUMENT RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Document download failed",
            "details": str(e)
        }
def update_ewaybill(awb_code, ewaybill_number):

    token, error = get_token()

    if error:
        return error

    url = f"{BASE_URL}/orders/ewaybill"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "awb": awb_code,
        "eway_bill_number": ewaybill_number
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("EWAY STATUS:", response.status_code)
        print("EWAY RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Ewaybill update failed",
            "details": str(e)
        }
def create_reverse_pickup(reverse_data):

    token, error = get_token()

    if error:
        return error

    url = f"{BASE_URL}/orders/create/return"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=reverse_data,
            timeout=20
        )

        print("REVERSE PICKUP STATUS:", response.status_code)
        print("REVERSE PICKUP RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "Reverse pickup creation failed",
            "details": str(e)
        }
def take_ndr_action(awb_code, action):

    token, error = get_token()

    if error:
        return error

    url = f"{BASE_URL}/ndr/action"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "awb": awb_code,
        "action": action
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("NDR STATUS:", response.status_code)
        print("NDR RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": "NDR action failed",
            "details": str(e)
        }