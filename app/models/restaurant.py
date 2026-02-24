from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    is_active = Column(Boolean, default=True)

    workplace_id = Column(Integer)

    start_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="restaurant") 

