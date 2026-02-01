from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from datetime import datetime
from database.db import Base

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_user_id = Column(Integer, ForeignKey("users.id"))
    reward_amount = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
