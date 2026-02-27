from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract
from database.db import get_db
from models.user import User
from models.order import Order
from models.restaurant import Restaurant
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy import and_, or_
from time import time
from lib_tu.timezone import SLOT_TIME_MAP


router = APIRouter(prefix="/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def admin_login(
    email_or_phone: str,
    password: str,
    db: Session = Depends(get_db)
):

    
    user = db.query(User).filter(
        or_(
            User.email == email_or_phone,
            User.phone == email_or_phone
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    if user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admin only")

    
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    
    access_token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

   
    return {
        "message": "Admin login successful",
        "role": user.role,
        "access_token": access_token
    }

# -----------------------------------ADMIN ORDERS------------------------------------

@router.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).join(User).all()

    
    if not orders:
        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )

    result = []

    for order in orders:
        result.append({
            "order_id": order.id,
            "customer_name": order.user.name,
            "customer_email": order.user.email,
            "total_amount": order.total_amount,
            "payable_amount": order.payable_amount,
            "status": order.status,
            "created_at": order.created_at
        })

    return result


# -------------------------REPORTS-------------------------------------------

@router.get("/admin/reports")
def get_reports(db: Session = Depends(get_db)):

    reports = (
        db.query(
            Order.id,
            Restaurant.name.label("restaurant_name"),
            Order.status,
            Order.created_at
        )
        .join(Restaurant, Order.restaurant_id == Restaurant.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    # ✅ 404 if no data
    if not reports:
        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )

    result = []

    for r in reports:
        result.append({
            "order_id": r.id,
            "restaurant_name": r.restaurant_name,
            "status": r.status,
            "order_month": r.created_at.strftime("%B"),
            "order_date": r.created_at.date(),
            "created_at": r.created_at
        })

    return result


# ----------------------------------------Available restaurant---------------------


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
