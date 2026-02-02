from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class DishUnit(Base):
    __tablename__ = "dish_units"

    id = Column(Integer, primary_key=True)

    unit_type = Column(String)  
    # KG / PIECES / PLATE

    measurement = Column(String)  
    # 0.5 KG / 1 KG / Full plate / Half plate

    quantity = Column(Integer, default=1)
    # how many (1,2,3...)

