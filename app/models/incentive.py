from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database.db import Base

class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="pending") 