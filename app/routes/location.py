from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from models.location import UserLocation
from pydantic import BaseModel, validator

router = APIRouter(prefix="/location", tags=["Location"])

class LocationSchema(BaseModel):
    user_id: int
    latitude: float
    longitude: float

    @validator("latitude")
    def validate_latitude(cls, v):
        if v < -90 or v > 90:
            raise ValueError("Invalid latitude")
        return v

    @validator("longitude")
    def validate_longitude(cls, v):
        if v < -180 or v > 180:
            raise ValueError("Invalid longitude")
        return v



@router.post("/")
def Create_location(data: LocationSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.latitude = data.latitude
    user.longitude = data.longitude
    db.commit()

    return {
        "message": "Location updated",
        "latitude": user.latitude,
        "longitude": user.longitude
    }