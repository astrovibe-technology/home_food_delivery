from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database.db import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  # user / cook / delivery / admin
    is_active = Column(Boolean, default=True)
    reset_otp = Column(String, nullable=True)
    is_otp_verified = Column(Boolean, default=False)
    otp_expiry = Column(DateTime, nullable=True)
    is_fake_mail = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




    referral_code = Column(String(20), unique=True, nullable=True)
    referred_by = Column(Integer, nullable=True)
    referral_count = Column(Integer, default=0)
    referral_earnings = Column(Integer, default=0)
