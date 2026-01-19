from sqlalchemy import Column, Integer, String
from database.db import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    is_active = Column(Integer, default=1)