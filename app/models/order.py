from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    total_amount = Column(Integer, default=0)