from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel


from database.db import SessionLocal
from models.cart import Cart
from models.shop import Shop
from routes.delivery_incentives import update_incentive
from datetime import date,timedelta
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

    # ✅ Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    added_items = []

    # ✅ Add / update items
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu {item.menu_id} not found")

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

    # ✅ SUBTOTAL CALCULATION ONLY
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    subtotal = 0

    for item in cart_items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        subtotal += menu.price * item.quantity

    # ✅ FINAL RESPONSE (NO GST / FEES)
    return {
        "message": "Items added to cart",
        "cart_id": cart.id,
        "items": added_items,
        "subtotal": round(subtotal, 2)
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



@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


# -----------------------------------------------CHECKOUT---------------------------------

class CheckoutRequest(BaseModel):
    user_id: int
    payment_method: str

    total_amount: float
    gst_food: float
    platform_fee: float
    gst_platform: float
    processing_fee: float
    payable_amount: float


@router.post("/checkout")
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db)
):
    user_id = request.user_id
    payment_method = request.payment_method

    # ✅ Validate payment method
    valid_methods = ["cod", "card", "upi"]
    if payment_method not in valid_methods:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # ✅ Get cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found")

    # ✅ Get cart items
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # ✅ Group items by shop
    shop_map = {}
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu {item.menu_id} not found")

        shop_id = menu.shop_id

        if shop_id not in shop_map:
            shop_map[shop_id] = []

        shop_map[shop_id].append((item, menu))

    orders_response = []

    # ✅ Create orders (per shop)
    for shop_id, item_list in shop_map.items():

        order = Order(
            user_id=user_id,
            shop_id=shop_id,

            # 🔥 Store frontend values (NO CALCULATION)
            total_amount=request.total_amount,
            gst_food=request.gst_food,
            platform_fee=request.platform_fee,
            gst_platform=request.gst_platform,
            processing_fee=request.processing_fee,
            payable_amount=request.payable_amount,

            payment_method=payment_method,
            payment_status="pending",
            status="pending"
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        order_items_data = []

        # ✅ Save order items
        for item, menu in item_list:
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
                "price": menu.price
            })

        # ✅ Payment status
        if payment_method == "cod":
            order.payment_status = "pending"
        else:
            order.payment_status = "paid"

        db.commit()

        orders_response.append({
            "order_id": order.id,
            "shop_id": shop_id,
            "total_amount": request.total_amount,
            "payable_amount": request.payable_amount,
            "payment_method": payment_method,
            "payment_status": order.payment_status,
            "items": order_items_data
        })


    update_incentive(db, user_id)

    # ✅ Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Orders placed successfully",
        "orders": orders_response
    }


# -------------------------------------------GET------------------------------------


@router.get("/checkout/orders")
def get_checkout_like_orders(
    user_id: int,
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Order).filter(Order.user_id == user_id)

    # ✅ CASE 1: only start_date (single day)
    if start_date and not end_date:
        query = query.filter(
            Order.created_at >= start_date,
            Order.created_at < (start_date + timedelta(days=1))
        )

    # ✅ CASE 2: only end_date
    elif end_date and not start_date:
        query = query.filter(
            Order.created_at < (end_date + timedelta(days=1))
        )

    # ✅ CASE 3: both start_date & end_date
    elif start_date and end_date:
        query = query.filter(
            Order.created_at >= start_date,
            Order.created_at < (end_date + timedelta(days=1))
        )

    orders = query.all()

    if not orders:
        return {"message": "No orders found"}

    shop_map = {}
    for order in orders:
        if order.shop_id not in shop_map:
            shop_map[order.shop_id] = []
        shop_map[order.shop_id].append(order)

    orders_response = []

    for shop_id, order_list in shop_map.items():

        shop = db.query(Shop).filter(Shop.id == shop_id).first()

        for order in order_list:

            items = db.query(OrderItem).filter(
                OrderItem.order_id == order.id
            ).all()

            order_items_data = []

            for item in items:
                menu = db.query(Menu).filter(Menu.id == item.menu_id).first()

                order_items_data.append({
                    "menu_id": item.menu_id,
                    "menu_name": menu.name if menu else None,
                    "quantity": item.quantity,
                    "price": item.price
                })

            orders_response.append({
                "order_id": order.id,
                "shop_id": shop_id,
                "shop_name": shop.shop_name if shop else None,

                "total_amount": order.total_amount,
                "gst_food": order.gst_food,
                "platform_fee": order.platform_fee,
                "gst_platform": order.gst_platform,
                "processing_fee": order.processing_fee,
                "payable_amount": order.payable_amount,

                "payment_method": order.payment_method,
                "payment_status": order.payment_status,
                "status": order.status,

                "created_at": order.created_at,
                "items": order_items_data
            })

    return {
        "message": "Orders fetched successfully",
        "total_orders": len(orders_response),
        "orders": orders_response
    }