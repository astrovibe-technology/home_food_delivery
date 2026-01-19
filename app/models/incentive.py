from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)
    reason = Column(String)