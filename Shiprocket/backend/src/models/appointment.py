from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from datetime import datetime
from src.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    service_name = Column(String, nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    google_event_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)