from sqlalchemy import Column, Integer, String, Boolean, Time
from database.db import Base

class Timing(Base):
    __tablename__ = "timings"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # earlymorning / lunch / dinner
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)