class CookingStatus(Base):
    __tablename__ = "cooking_status"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_cooking_today = Column(Boolean, default=False)
    date = Column(Date)