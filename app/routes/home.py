# from fastapi import APIRouter, Depends, Query, HTTPException, status
# from sqlalchemy.orm import Session
# from datetime import date
# from time import time
# from database.restaurant import RestaurantCreate, RestaurantResponse
# from sqlalchemy import and_, or_

# from database.db import get_db
# from models.restaurant import Restaurant
# from lib_tu.timezone import SLOT_TIME_MAP

# router = APIRouter(prefix="/home", tags=["Home"])


# @router.post(
#     "",
#     response_model=RestaurantResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_restaurant(
#     payload: RestaurantCreate,
#     db: Session = Depends(get_db)
# ):
#     # Validation
#     if payload.start_time >= payload.end_time:
#         raise HTTPException(
#             status_code=400,
#             detail="start_time must be earlier than end_time"
#         )

#     restaurant = Restaurant(
#         name=payload.name,
#         address=payload.address,
#         # workplace_id=payload.workplace_id,
#         start_date=payload.start_date or date.today(),
#         start_time=payload.start_time,
#         end_time=payload.end_time,
#         is_active=True
#     )

#     db.add(restaurant)
#     db.commit()
#     db.refresh(restaurant)

#     return restaurant

