from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from models.order import Order
from models.orderitem import OrderItem
from database.db import get_db

router = APIRouter(prefix="/order_status", tags=["order_status"])




@router.get("/orders/pending")
def get_all_pending_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(
        Order.status == "pending"
    ).order_by(Order.id.desc()).all()

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




@router.get("/orders/completed")
def get_all_completed_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(
        Order.status == "completed"
    ).order_by(Order.id.desc()).all()

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







