from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_,func
from typing import List
from datetime import date
from pydantic import BaseModel
from database.db import get_db
from models.order import Order
from models.user import User
from models.shop import Shop
from models.incentive import Incentive
from models.activity import UserActivity



router = APIRouter(prefix="/dashboard", tags=["dashboard"])





@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "user_id": order.user_id,
        "address_id": order.address_id,
        "total_amount": order.total_amount,
        "discount_amount": order.discount_amount,
        "payable_amount": order.payable_amount,
        "status": order.status,
        "created_at": order.created_at,

        "restaurant_id": order.restaurant_id,
        "shop_id": order.shop_id,

        # "razorpay_order_id": order.razorpay_order_id,
        # "razorpay_payment_id": order.razorpay_payment_id,
        # "razorpay_signature": order.razorpay_signature,

        "payment_status": order.payment_status,
        "payment_method": order.payment_method,

        "gst_food": order.gst_food,
        "platform_fee": order.platform_fee,
        "gst_platform": order.gst_platform,
        "processing_fee": order.processing_fee
    }


# ----------------------------- user search---------------------------------------------------


@router.get("/admin/users/search")
def search_users(query: str, db: Session = Depends(get_db)):

    users = db.query(User).filter(
        or_(
            User.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%"),
            User.phone.ilike(f"%{query}%"),
            User.id == int(query) if query.isdigit() else False
        )
    ).all()

    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone
        } for u in users
    ]


# ---------------------------------- Activity History ----------------------------------

@router.get("/admin/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_users = db.query(func.count(User.id)).scalar()

    kitchen_users = db.query(func.count(Shop.id)).scalar()

    today = date.today()

    today_sales = db.query(func.sum(Order.total_amount)).filter(
        func.date(Order.created_at) == today
    ).scalar() or 0

    month_start = today.replace(day=1)

    monthly_sales = db.query(func.sum(Order.total_amount)).filter(
        Order.created_at >= month_start
    ).scalar() or 0

    return {
        "total_users": total_users,
        "kitchen_users": kitchen_users,
        "today_sales": today_sales,
        "monthly_sales": monthly_sales
    }



@router.get("/admin/incentives/pending")
def pending_incentives(db: Session = Depends(get_db)):
    return db.query(Incentive).filter(Incentive.status == "pending").all()


@router.put("/admin/incentives/{id}/approve")
def approve_incentive(id: int, db: Session = Depends(get_db)):

    inc = db.query(Incentive).get(id)
    if not inc:
        raise HTTPException(404, "Not found")

    inc.status = "approved"

    user = db.query(User).get(inc.user_id)
    if user:
        user.incentives += inc.amount   # ✅ now works

    db.commit()

    return {"message": "Incentive approved"}