from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db import SessionLocal
from models.cart import Cart
from models.cartitem import CartItem
from models.menu import Menu
from models.order import Order
from models.restaurant import Restaurant
from models.orderitem import OrderItem

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
   
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

   
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

  
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

    # 1️⃣ Get Cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2️⃣ Get Cart Items
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="No items in cart")

    total = 0
    order_items_response = []

    # 3️⃣ Get Restaurant ID from First Menu
    first_menu = db.query(Menu).filter(Menu.id == items[0].menu_id).first()
    if not first_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    restaurant_id = first_menu.restaurant_id

    # 4️⃣ Safety Check – Prevent Multiple Restaurants
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu id {item.menu_id} not found")

        if menu.restaurant_id != restaurant_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot checkout items from multiple restaurants"
            )

    # 5️⃣ Create Order (🔥 FIXED – restaurant_id added)
    order = Order(
        user_id=user_id,
        restaurant_id=restaurant_id,  # ✅ FIX HERE
        total_amount=0,
        payable_amount=0,
        status="pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # 6️⃣ Create Order Items
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()

        item_total = item.quantity * menu.price
        total += item_total

        order_item = OrderItem(
            order_id=order.id,
            menu_id=menu.id,
            quantity=item.quantity,
            price=menu.price
        )
        db.add(order_item)

        order_items_response.append({
            "menu_id": menu.id,
            "menu_name": menu.name,
            "price": menu.price,
            "quantity": item.quantity,
            "total": item_total
        })

    # 7️⃣ Update Order Amount
    order.total_amount = total
    order.payable_amount = total

    # 8️⃣ Clear Cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()

    return {
        "order_id": order.id,
        "restaurant_id": restaurant_id, 
        "status": order.status,
        "items": order_items_response,
        "total_amount": total,
        "message": "Order placed successfully"
    }



