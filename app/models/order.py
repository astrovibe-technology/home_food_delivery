from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    shop_id = Column(Integer, ForeignKey("shops.id")) 
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))
    total_amount = Column(Integer, default=0)
    discount_amount = Column(Integer, default=0)
    payable_amount = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=True)
    payment_status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")