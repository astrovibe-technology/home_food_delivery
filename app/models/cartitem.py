class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"))
    quantity = Column(Integer, default=1)