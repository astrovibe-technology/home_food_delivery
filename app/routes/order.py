from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.order import Order
from models.orderitem import OrderItem

router = APIRouter(prefix="/orders", tags=["Order"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Allowed flow map
STATUS_FLOW = {
    "pending": ["preparing", "cancelled"],
    "preparing": ["packed", "cancelled"],
    "packed": ["out_for_delivery", "cancelled"],
    "out_for_delivery": ["completed"],
    "completed": [],
    "cancelled": []
}


@router.put("/{order_id}/status")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order.status.lower()
    new_status = new_status.lower()

    # Validate status exists
    if new_status not in STATUS_FLOW:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {list(STATUS_FLOW.keys())}"
        )

    # Validate flow
    if new_status not in STATUS_FLOW[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change from '{current_status}' → '{new_status}'"
        )

    order.status = new_status
    db.commit()

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "old_status": current_status,
        "new_status": new_status
    }




@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).order_by(Order.id.desc()).all()

    result = []

    for order in orders:
        # Count items in this order
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

    return {
        "total_orders": len(result),
        "orders": result
    }

