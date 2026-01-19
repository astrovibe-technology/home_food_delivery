from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))