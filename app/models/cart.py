from sqlalchemy import Column, Integer, ForeignKey
from database.db import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"))
    quantity = Column(Integer, default=1)