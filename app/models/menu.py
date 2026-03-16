from sqlalchemy import Column, Integer, String, Boolean , ForeignKey
from database.db import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    shop_id = Column(Integer, ForeignKey("shops.id")) 
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

    created_by = Column(Integer, ForeignKey("users.id"))