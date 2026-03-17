from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel


from database.db import SessionLocal
from models.cart import Cart
from models.cooking_dish import CookingDish
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
class CartItemRequest(BaseModel):
    menu_id: int
    quantity: int

class AddToCartRequest(BaseModel):
    user_id: int
    items: List[CartItemRequest]


@router.post("/add")
def add_multiple_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db)
):
    user_id = request.user_id
    items = request.items

    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    added_items = []

    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu {item.menu_id} not found")

        # Check existing item
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.menu_id == item.menu_id
        ).first()

        if existing_item:
            existing_item.quantity += item.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                menu_id=item.menu_id,
                quantity=item.quantity
            )
            db.add(cart_item)

        added_items.append({
            "menu_id": item.menu_id,
            "quantity": item.quantity
        })

    db.commit()

    return {
        "message": "Items added to cart",
        "cart_id": cart.id,
        "items": added_items
    }

# ----------------------------------- GET -----------------------------------------------

@router.get("/get")
def get_user_cart(
    user_id: int,
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return {
            "user_id": user_id,
            "cart": [],
            "total_amount": 0
        }

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    cart_data = []
    total_amount = 0

    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()

        item_total = menu.price * item.quantity
        total_amount += item_total

        cart_data.append({
            "menu_id": menu.id,
            "name": menu.name,
            "price": menu.price,
            "quantity": item.quantity,
            "total": item_total
        })

    return {
        "user_id": user_id,
        "cart_id": cart.id,
        "total_items": len(cart_data),
        "total_amount": total_amount,
        "items": cart_data
    }



# @router.get("/{user_id}")
# def view_cart(user_id: int, db: Session = Depends(get_db)):
#     cart = db.query(Cart).filter(Cart.user_id == user_id).first()
#     if not cart:
#         return {"items": [], "total_amount": 0}

#     items = db.query(CartItem, Menu).join(Menu, CartItem.menu_id == Menu.id).filter(
#         CartItem.cart_id == cart.id
#     ).all()

#     total = 0
#     data = []

#     for item, menu in items:
#         item_total = item.quantity * menu.price
#         total += item_total
#         data.append({
#             "item_id": item.id,
#             "menu_id": menu.id,
#             "menu_name": menu.name,
#             "price": menu.price,
#             "quantity": item.quantity,
#             "total": item_total
#         })

#     return {
#         "cart_id": cart.id,
#         "items": data,
#         "total_amount": total
#     }


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



@router.post("/cart/checkout")
def checkout(user_id: int, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found")

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 🔥 GROUP ITEMS BY SHOP
    shop_map = {}

    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()

        shop_id = menu.shop_id

        if shop_id not in shop_map:
            shop_map[shop_id] = []

        shop_map[shop_id].append((item, menu))

    orders_response = []

    # 🔥 CREATE ORDER PER SHOP
    for shop_id, item_list in shop_map.items():

        total = 0

        order = Order(
            user_id=user_id,
            shop_id=shop_id,
            total_amount=0,
            payable_amount=0,
            status="pending"
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        order_items_data = []

        for item, menu in item_list:

            item_total = menu.price * item.quantity
            total += item_total

            order_item = OrderItem(
                order_id=order.id,
                menu_id=menu.id,
                quantity=item.quantity,
                price=menu.price
            )

            db.add(order_item)

            order_items_data.append({
                "menu_id": menu.id,
                "menu_name": menu.name,
                "quantity": item.quantity,
                "price": menu.price,
                "total": item_total
            })

        order.total_amount = total
        order.payable_amount = total

        db.commit()

        orders_response.append({
            "order_id": order.id,
            "shop_id": shop_id,
            "total_amount": total,
            "items": order_items_data
        })

    # 🧹 CLEAR CART
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Orders placed successfully (multi-shop)",
        "orders": orders_response
    }

