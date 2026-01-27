from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class RestaurantCreate(BaseModel):
    name: str
    address: Optional[str] = None
    workplace_id: Optional[int] = None
    start_date: Optional[date] = None
    start_time: time
    end_time: time

class RestaurantResponse(BaseModel):
    id: int
    name: str
    workplace_id: int | None
    start_date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

