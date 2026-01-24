from sqlalchemy import Column, Integer, Boolean, String
from database.db import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)