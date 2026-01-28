from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db import SessionLocal
from models.cart import Cart
from models.cartitem import CartItem
from models.menu import Menu
from models.order import Order

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------ADD------------------------------------------

@router.post("/add")
def add_to_cart(
    user_id: int,
    menu_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    # Fetch menu by ID
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Check if item already in cart
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_id == menu.id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            menu_id=menu.id,
            quantity=quantity
        )
        db.add(item)

    db.commit()

    return {
        "message": "Item added to cart",
        "menu_name": menu.name,
        "quantity": quantity
    }

# ----------------------------------- GET -----------------------------------------------


@router.get("/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return {"items": [], "total_amount": 0}

    items = db.query(CartItem, Menu).join(Menu, CartItem.menu_id == Menu.id).filter(
        CartItem.cart_id == cart.id
    ).all()

    total = 0
    data = []

    for item, menu in items:
        item_total = item.quantity * menu.price
        total += item_total
        data.append({
            "item_id": item.id,
            "menu_id": menu.id,
            "menu_name": menu.name,
            "price": menu.price,
            "quantity": item.quantity,
            "total": item_total
        })

    return {
        "cart_id": cart.id,
        "items": data,
        "total_amount": total
    }


# ---------------------------------------------- PUT-----------------------

@router.put("/item/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if quantity < 1:
        db.delete(item)
    else:
        item.quantity = quantity

    db.commit()
    return {"message": "Cart updated"}


# --------------------------------------DELETE-------------------------------------

@router.delete("/item/{item_id}")
def remove_cart_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}


# -----------------------------------------------CHECKOUT---------------------------------



@router.post("/checkout")
def checkout(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="No items in cart")

    # Calculate total
    total = 0
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        total += item.quantity * menu.price

    # Create order
    order = Order(user_id=user_id, total_amount=total, status="PENDING")
    db.add(order)

    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {"order_id": order.id, "amount": total, "message": "Proceed to payment"}