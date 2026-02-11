from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database.db import Base

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)   # SAVE50
    discount_type = Column(String)  # FLAT / PERCENT
    discount_value = Column(Integer)  # 50 or 10
    is_active = Column(Boolean, default=True)

    created_by = Column(Integer, ForeignKey("users.id"))