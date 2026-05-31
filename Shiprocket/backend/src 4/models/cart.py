from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from src.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
