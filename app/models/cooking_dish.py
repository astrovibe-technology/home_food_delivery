from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from database.db import Base

class CookingDish(Base):
    __tablename__ = "cooking_dishes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    dish_type = Column(String)  # SOCIETY / WORKPLACE / TRAVEL

    title = Column(String, nullable=False)
    food_type = Column(String)  # VEG / NON_VEG
    is_halal = Column(Boolean, default=False)
    halal_certificate = Column(String, nullable=True)

    description = Column(String)
    price = Column(Integer)

    delivery_datetime = Column(DateTime)
    last_order_time = Column(DateTime)

    # Society / Workplace
    building_name = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    floor_number = Column(String, nullable=True)

    # Travel
    travel_type = Column(String, nullable=True)  # TRAIN / BUS
    train_name = Column(String, nullable=True)
    train_number = Column(String, nullable=True)
    bus_number = Column(String, nullable=True)
    route = Column(String, nullable=True)
    bogie_number = Column(String, nullable=True)
    seat_number = Column(String, nullable=True)

    is_published = Column(Boolean, default=False)