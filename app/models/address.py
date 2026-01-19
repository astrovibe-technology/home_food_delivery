from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # home / workplace / society / travel
    address = Column(String)