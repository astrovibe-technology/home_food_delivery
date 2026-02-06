from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from database.db import Base
from datetime import date

class DeliveryIncentive(Base):
    __tablename__ = "delivery_incentives"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    week_start = Column(Date)        # Monday date
    week_orders = Column(Integer, default=0)
    week_reward_given = Column(Boolean, default=False)

    month = Column(Integer)          # 1–12
    year = Column(Integer)
    month_orders = Column(Integer, default=0)
    month_reward_given = Column(Boolean, default=False)

    lifetime_orders = Column(Integer, default=0)
    lifetime_reward_given = Column(Boolean, default=False)