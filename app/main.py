import os
import time
from fastapi import FastAPI


from models.user import User
from models.restaurant import Restaurant
from models.menu import Menu
from models.cart import Cart
from models.cartitem import CartItem
from models.address import Address
from models.order import Order       
from models.orderitem import OrderItem 
from models.promocode import PromoCode
from models.shop import Shop

# Routers
from routes.user import router as auth_router
from routes.home import router as home_router
from routes.cart import router as cart_router
from routes.menu import router as menu_router
from routes.promocode import router as promocode_router
from routes.shop import router as shop_router


from database.db import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(home_router)
app.include_router(cart_router)
app.include_router(menu_router)
app.include_router(promocode_router)
app.include_router(shop_router)
