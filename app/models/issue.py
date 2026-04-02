from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database.db import Base
from datetime import datetime

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    issue_type = Column(String(50))  # bug / complaint / feedback
    status = Column(String(50), default="open")  # open / resolved

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)