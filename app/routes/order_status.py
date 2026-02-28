from sqlalchemy.orm import Session
from sqlalchemy import func
import pytz
# from datetime import time
from datetime import date,datetime,time,timedelta
from fastapi import APIRouter, Depends, HTTPException
from models.order import Order
from models.orderitem import OrderItem
from database.db import get_db

router = APIRouter(prefix="/order_status", tags=["order_status"])

# ------------------------------------ PENDING -----------------------------------------


@router.get("/orders/pending")
def get_all_pending_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(
        Order.status == "pending"
    ).order_by(Order.id.desc()).all()

    
    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No pending orders found"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result



@router.get("/orders/pending/today")
def get_today_pending_orders(db: Session = Depends(get_db)):

    today = date.today()

    orders = db.query(Order).filter(
        Order.status == "pending",
        Order.created_at >= today
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No pending orders found for today")

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result



@router.get("/orders/pending/by-date")
def get_pending_orders_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):

    # Convert start_date to datetime 00:00:00
    start_datetime = datetime(start_date.year, start_date.month, start_date.day)

    # Convert end_date to next day 00:00:00
    end_datetime = datetime(end_date.year, end_date.month, end_date.day) + timedelta(days=1)

    orders = db.query(Order).filter(
        Order.status == "pending",
        Order.created_at >= start_datetime,
        Order.created_at < end_datetime   # important (< next day)
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No pending orders found for given date range"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result

# ---------------------------------- PENDING -------------------------------------------

@router.get("/orders/completed")
def get_all_completed_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(
        Order.status == "completed"
    ).order_by(Order.id.desc()).all()

    
    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No completed orders found"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result





@router.get("/orders/completed/today")
def get_today_completed_orders(db: Session = Depends(get_db)):

    today_utc = datetime.utcnow().date()

    orders = db.query(Order).filter(
        Order.status == "completed",
        func.date(Order.created_at) == today_utc
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No completed orders found for today"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result




@router.get("/orders/completed/by-date")
def get_completed_orders_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    orders = db.query(Order).filter(
        Order.status == "completed",
        Order.created_at.between(start_datetime, end_datetime)
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No completed orders found for given date range"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result




# ----------------------------- COMPLETED ---------------------------------------------

@router.get("/orders/cancelled")
def get_all_cancelled_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(
        Order.status == "cancelled"
    ).order_by(Order.id.desc()).all()

   
    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No cancelled orders found"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result



@router.get("/orders/cancelled/today")
def get_today_cancelled_orders(db: Session = Depends(get_db)):

    # Current UTC time
    now = datetime.utcnow()

    # Start of today (UTC)
    start_of_day = datetime(now.year, now.month, now.day)

    # End of today (UTC)
    end_of_day = start_of_day + timedelta(days=1)

    orders = db.query(Order).filter(
        Order.status == "cancelled",
        Order.created_at >= start_of_day,
        Order.created_at < end_of_day
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No cancelled orders found for today"
        )

    return orders



@router.get("/orders/cancelled/by-date")
def get_cancelled_orders_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    orders = db.query(Order).filter(
        Order.status == "cancelled",
        Order.created_at.between(start_datetime, end_datetime)
    ).order_by(Order.id.desc()).all()

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No cancelled orders found for given date range"
        )

    result = []

    for order in orders:
        item_count = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).count()

        result.append({
            "order_id": order.id,
            "items": item_count,
            "amount": order.total_amount,
            "date": order.created_at,
            "status": order.status
        })

    return result





