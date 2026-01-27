from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from time import time
from database.restaurant import RestaurantCreate, RestaurantResponse
from sqlalchemy import and_, or_

from database.db import get_db
from models.restaurant import Restaurant
from lib_tu.timezone import SLOT_TIME_MAP

router = APIRouter(prefix="/home", tags=["Home"])


@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db)
):
    # Validation
    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time must be earlier than end_time"
        )

    restaurant = Restaurant(
        name=payload.name,
        address=payload.address,
        # workplace_id=payload.workplace_id,
        start_date=payload.start_date or date.today(),
        start_time=payload.start_time,
        end_time=payload.end_time,
        is_active=True
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant

@router.get("/restaurants")
def get_available_restaurants(
    slot: str = Query(..., description=" Early Morning / breakfast / lunch / dinner / Brunch / Snacks / Midnight "),
    db: Session = Depends(get_db)
):
    slot = slot.lower()

    if slot not in SLOT_TIME_MAP:
        raise HTTPException(
            status_code=400,
            detail="Invalid slot. Please select a valid time slot."
        )

    start_time, end_time = SLOT_TIME_MAP[slot]

    # midnight special case
    if slot == "midnight":
        restaurants = db.query(Restaurant).filter(
            Restaurant.is_active == True,
            or_(
                and_(Restaurant.start_time <= start_time, Restaurant.end_time <= time(23,59)),
                and_(Restaurant.start_time >= time(0,0), Restaurant.end_time >= end_time)
            )
        ).all()
    else:
        restaurants = db.query(Restaurant).filter(
            Restaurant.is_active == True,
            Restaurant.start_time <= start_time,
            Restaurant.end_time >= end_time
        ).all()

    if not restaurants:
        raise HTTPException(
            status_code=404,
            detail=f"No restaurants available for {slot} time."
        )

    return {
        "slot": slot,
        "count": len(restaurants),
        "restaurants": restaurants
    }