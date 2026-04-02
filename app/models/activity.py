from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.db import Base

class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(String)
    performed_by = Column(String)  # admin / user / agent
    created_at = Column(DateTime, default=datetime.utcnow)