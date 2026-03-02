from typing import Optional
from datetime import datetime, date, time, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import pytz

from database.db import get_db
from models.order import Order
from models.orderitem import OrderItem

router = APIRouter(prefix="/order_status", tags=["order_status"])



def get_orders_by_status(
    status: str,
    db: Session,
    start_date: Optional[str],
    end_date: Optional[str]
):
    query = db.query(Order).filter(Order.status == status)

    ist = pytz.timezone("Asia/Kolkata")

    
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        query = query.filter(
            Order.created_at >= start,
            Order.created_at < end
        )

    
    elif start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(days=1)

        query = query.filter(
            Order.created_at >= start,
            Order.created_at < end
        )

    
    elif end_date:
        start = datetime.strptime(end_date, "%Y-%m-%d")
        end = start + timedelta(days=1)

        query = query.filter(
            Order.created_at >= start,
            Order.created_at < end
        )

    
    else:
        today = datetime.now(ist).date()

        start = datetime.combine(today, time.min)
        end = start + timedelta(days=1)

        query = query.filter(
            Order.created_at >= start,
            Order.created_at < end
        )

    orders = query.order_by(Order.id.desc()).all()

    
    if not orders:
        raise HTTPException(
            status_code=404,
            detail="No data found"
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


# ---------------- PENDING ----------------

@router.get("/orders/pending")
def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_orders_by_status("pending", db, start_date, end_date)


# ---------------- COMPLETED ----------------

@router.get("/orders/completed")
def get_completed_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_orders_by_status("completed", db, start_date, end_date)


# ---------------- CANCELLED ----------------

@router.get("/orders/cancelled")
def get_cancelled_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_orders_by_status("cancelled", db, start_date, end_date)