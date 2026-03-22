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


STATUS_FLOW = {
    "pending": ["preparing", "completed", "cancelled"], 
    "preparing": ["packed", "completed", "cancelled"],
    "packed": ["out_for_delivery", "completed", "cancelled"],
    "out_for_delivery": ["completed", "cancelled"],
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


    if new_status not in STATUS_FLOW:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {list(STATUS_FLOW.keys())}"
        )


    if current_status in ["completed", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status once order is '{current_status}'"
        )


    if new_status not in STATUS_FLOW[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change from '{current_status}' → '{new_status}'"
        )

    order.status = new_status
    db.commit()

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "old_status": current_status,
        "new_status": new_status
    }




@router.get("/orders/bought")
def get_bought_orders(
    user_id: int,
    status: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Order).filter(Order.user_id == user_id)

    if status:
        query = query.filter(Order.status == status.lower())

    orders = query.all()

    if not orders:
        return {"message": "No bought orders found"}

    result = []

    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        result.append({
            "order_id": order.id,
            "shop_id": order.shop_id,
            "total_amount": order.total_amount,
            "payment_method": order.payment_method,
            "payment_status": order.payment_status,
            "status": order.status,
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else None,  # 👈 NEW
            "items": [
                {
                    "menu_id": item.menu_id,
                    "quantity": item.quantity,
                    "price": item.price
                } for item in items
            ]
        })

    return {
        "type": "bought",
        "orders": result
    }



@router.get("/orders/sold")
def get_sold_orders(
    shop_id: int,
    status: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Order).filter(Order.shop_id == shop_id)

    if status:
        query = query.filter(Order.status == status.lower())

    orders = query.all()

    if not orders:
        return {"message": "No sold orders found"}

    result = []

    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        result.append({
            "order_id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "payment_method": order.payment_method,
            "payment_status": order.payment_status,
            "status": order.status,
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else None,  # 👈 NEW
            "items": [
                {
                    "menu_id": item.menu_id,
                    "quantity": item.quantity,
                    "price": item.price
                } for item in items
            ]
        })

    return {
        "type": "sold",
        "orders": result
    }

