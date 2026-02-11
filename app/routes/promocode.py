from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.promocode import PromoCode
from models.order import Order
from models.user import User

router = APIRouter(prefix="/promocode", tags=["Promocode"])


@router.post("/add")
def add_promo(
    user_id: int,  
    code: str,
    discount_type: str,
    discount_value: int,
    db: Session = Depends(get_db)
):
    existing = db.query(PromoCode).filter(
        PromoCode.code == code.upper()
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")

    promo = PromoCode(
        code=code.upper(),
        discount_type=discount_type.upper(),
        discount_value=discount_value,
        is_active=True,
        created_by=user_id      
    )

    db.add(promo)
    db.commit()
    db.refresh(promo)

    return {
        "message": "Promo code added successfully",
        "code": promo.code,
        "created_by": promo.created_by
    }


@router.post("/apply")
def apply_promo(
    order_id: int,
    promo_code: str,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.discount_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="Promo already applied to this order"
        )

    promo = db.query(PromoCode).filter(
        PromoCode.code == promo_code.upper(),
        PromoCode.is_active == True
    ).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Invalid promo code")

    if promo.discount_type == "FLAT":
        discount = promo.discount_value

    elif promo.discount_type == "PERCENT":
        discount = (order.total_amount * promo.discount_value) // 100

    else:
        raise HTTPException(status_code=400, detail="Invalid discount type")

    payable = max(order.total_amount - discount, 0)

    order.discount_amount = discount
    order.payable_amount = payable

    db.commit()

    return {
        "message": "Promo applied successfully",
        "total_amount": order.total_amount,
        "discount": discount,
        "payable_amount": payable
    }