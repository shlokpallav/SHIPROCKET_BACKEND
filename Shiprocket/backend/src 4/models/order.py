from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
