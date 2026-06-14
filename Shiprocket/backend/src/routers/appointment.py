from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time

from src.database import get_db
from src.models.appointment import Appointment
from src.routers.calendar import create_calendar_event

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/book")
def book_appointment(
    customer_name: str,
    service_name: str,
    appointment_date: date,
    start_time: time,
    end_time: time,
    customer_phone: str = None,
    customer_email: str = None,
    db: Session = Depends(get_db)
):
    if end_time <= start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    existing_appointment = db.query(Appointment).filter(
        Appointment.appointment_date == appointment_date,
        Appointment.start_time == start_time
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="This time slot is already booked"
        )

    total_appointments = db.query(Appointment).count()

    if total_appointments >= 30:
        oldest_appointment = db.query(Appointment).order_by(
            Appointment.created_at.asc()
        ).first()

        if oldest_appointment:
            db.delete(oldest_appointment)
            db.commit()

    start_datetime = f"{appointment_date}T{start_time}+05:30"
    end_datetime = f"{appointment_date}T{end_time}+05:30"

    event_link = create_calendar_event(
        summary=f"{service_name} - {customer_name}",
        description=(
            f"Customer Name: {customer_name}\n"
            f"Customer Phone: {customer_phone}\n"
            f"Customer Email: {customer_email}\n"
            f"Service: {service_name}"
        ),
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )

    appointment = Appointment(
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        service_name=service_name,
        appointment_date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        google_event_link=event_link
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id,
        "google_event_link": appointment.google_event_link
    }


@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).order_by(
        Appointment.created_at.desc()
    ).all()


@router.get("/available-slots")
def get_available_slots(
    appointment_date: date,
    db: Session = Depends(get_db)
):
    all_slots = [
        "09:00:00",
        "09:30:00",
        "10:00:00",
        "10:30:00",
        "11:00:00",
        "11:30:00",
        "12:00:00",
        "12:30:00",
        "14:00:00",
        "14:30:00",
        "15:00:00",
        "15:30:00",
        "16:00:00",
        "16:30:00",
        "17:00:00",
    ]

    booked_appointments = db.query(Appointment).filter(
        Appointment.appointment_date == appointment_date
    ).all()

    booked_slots = [
        str(appointment.start_time)
        for appointment in booked_appointments
    ]

    available_slots = [
        slot for slot in all_slots
        if slot not in booked_slots
    ]

    return {
        "date": appointment_date,
        "available_slots": available_slots
    }


@router.put("/{appointment_id}/reschedule")
def reschedule_appointment(
    appointment_id: int,
    new_date: date,
    new_start_time: time,
    new_end_time: time,
    db: Session = Depends(get_db)
):
    if new_end_time <= new_start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    existing_appointment = db.query(Appointment).filter(
        Appointment.appointment_date == new_date,
        Appointment.start_time == new_start_time,
        Appointment.id != appointment_id
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="This new time slot is already booked"
        )

    appointment.appointment_date = new_date
    appointment.start_time = new_start_time
    appointment.end_time = new_end_time

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment rescheduled successfully",
        "appointment_id": appointment.id,
        "new_date": appointment.appointment_date,
        "new_start_time": appointment.start_time,
        "new_end_time": appointment.end_time
    }


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted successfully"}