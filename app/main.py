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
from models.cooking_dish import CookingDish
from models.referral import Referral
from models.unit import DishUnit
from models.type import Type
from models.timings import Timing
from models.delivery_incentive import DeliveryIncentive
from models.location import UserLocation

# Routers
from routes.user import router as auth_router
# from routes.home import router as home_router
from routes.cart import router as cart_router
from routes.menu import router as menu_router
from routes.promocode import router as promocode_router
from routes.shop import router as shop_router
from routes.cooking_dish import router as cooking_dish_router
from routes.referral import router as referral_router
from routes.unit import router  as unit_router
from routes.type import router  as type_router
from routes.timings import router as timings_router
from routes.order import router as orderrouter
from routes.delivery_incentives import router as delivery_incentives_router
from routes.order_status import router as order_status_router
from routes.admin import router as admin_router
from routes.location import router as location_router



from database.db import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(admin_router)
app.include_router(auth_router)
# app.include_router(home_router)
app.include_router(cart_router)
app.include_router(menu_router)
app.include_router(promocode_router)
app.include_router(shop_router)
app.include_router(cooking_dish_router)
app.include_router(referral_router)
app.include_router(unit_router)
app.include_router(type_router)
app.include_router(timings_router)
app.include_router(orderrouter)
app.include_router(order_status_router)
app.include_router( delivery_incentives_router)
app.include_router(location_router)