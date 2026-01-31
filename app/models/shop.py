from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    shop_name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    certificate_no = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)

    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    IFSC_Code = Column(String, nullable=True)