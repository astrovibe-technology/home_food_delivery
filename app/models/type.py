from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    # WORKPLACE / SOCIETY / TRAVEL

    is_active = Column(Boolean, default=True)