from sqlalchemy import Column, Integer, String
from database.db import Base

class PoolingOrder(Base):
    __tablename__ = "pooling_orders"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    max_people = Column(Integer)
    status = Column(String, default="open")  # open / closed