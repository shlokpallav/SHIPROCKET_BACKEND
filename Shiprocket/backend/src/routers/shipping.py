from fastapi import APIRouter

from src.services.shiprocket_service import (
    shiprocket_login,
    check_serviceability,
    calculate_shipping_cost,
    create_order,
    track_shipment,
    generate_label,
    create_pickup_request,
    cancel_shipment,
    update_shipment,
    download_document,
    update_ewaybill,
    create_reverse_pickup,
    take_ndr_action
)

router = APIRouter(
    prefix="/shipping",
    tags=["Shipping"]
)


@router.get("/test")
def test_shipping():
    return {"message": "Shipping router working"}


@router.post("/login")
def login():
    return shiprocket_login()


@router.get("/serviceability")
def serviceability(
    pickup_pincode: int,
    delivery_pincode: int,
    weight: float,
    cod: int
):
    return check_serviceability(
        pickup_pincode,
        delivery_pincode,
        weight,
        cod
    )


@router.get("/shipping-cost")
def shipping_cost(
    pickup_pincode: int,
    delivery_pincode: int,
    weight: float,
    cod: int
):
    return calculate_shipping_cost(
        pickup_pincode,
        delivery_pincode,
        weight,
        cod
    )


@router.post("/create-order")
def create_shipment():
    order_data = {
        "order_id": "ORDER_101",
        "order_date": "2026-05-26",
        "pickup_location": "Home",
        "billing_customer_name": "Shlok",
        "billing_last_name": "Pallav",
        "billing_address": "Delhi",
        "billing_city": "Delhi",
        "billing_pincode": "110001",
        "billing_state": "Delhi",
        "billing_country": "India",
        "billing_email": "test@gmail.com",
        "billing_phone": "7007132470",
        "shipping_is_billing": True,
        "order_items": [
            {
                "name": "Tshirt",
                "sku": "TSHIRT001",
                "units": 1,
                "selling_price": 500
            }
        ],
        "payment_method": "Prepaid",
        "sub_total": 500,
        "length": 10,
        "breadth": 10,
        "height": 10,
        "weight": 0.5
    }

    return create_order(order_data)


@router.get("/track/{awb_code}")
def track_order(awb_code: str):
    return track_shipment(awb_code)


@router.post("/generate-label/{shipment_id}")
def create_label(shipment_id: int):
    return generate_label(shipment_id)


@router.post("/pickup-request/{shipment_id}")
def pickup_request(shipment_id: int):
    return create_pickup_request(shipment_id)


@router.post("/cancel-shipment/{awb_code}")
def cancel_order(awb_code: str):
    return cancel_shipment(awb_code)


@router.post("/update-shipment/{shipment_id}")
def update_order(shipment_id: int):
    update_data = {
        "billing_customer_name": "Updated Name",
        "billing_phone": "9999999999",
        "billing_address": "Updated Address"
    }

    return update_shipment(
        shipment_id,
        update_data
    )


@router.get("/download-document/{shipment_id}")
def download_invoice(shipment_id: int):
    return download_document(shipment_id)
@router.post("/update-ewaybill/{awb_code}")
def ewaybill_update(awb_code: str):

    ewaybill_number = "123456789"

    return update_ewaybill(
        awb_code,
        ewaybill_number
    )
@router.post("/reverse-pickup")
def reverse_pickup():

    reverse_data = {
        "order_id": "RETURN_ORDER_101",
        "order_date": "2026-05-26",
        "pickup_customer_name": "Shlok",
        "pickup_last_name": "Pallav",
        "pickup_address": "Delhi",
        "pickup_city": "Delhi",
        "pickup_state": "Delhi",
        "pickup_country": "India",
        "pickup_pincode": "110001",
        "pickup_email": "test@gmail.com",
        "pickup_phone": "7007132470",
        "order_items": [
            {
                "name": "Tshirt",
                "sku": "TSHIRT001",
                "units": 1,
                "selling_price": 500
            }
        ],
        "payment_method": "Prepaid",
        "sub_total": 500,
        "length": 10,
        "breadth": 10,
        "height": 10,
        "weight": 0.5
    }

    return create_reverse_pickup(reverse_data)
@router.post("/ndr-action/{awb_code}")
def ndr_action(awb_code: str):

    action = "reattempt"

    return take_ndr_action(
        awb_code,
        action
    )