from database.db import engine, Base
from models.user import User
from models.address import Address
from models.cart import Cart
from models.cartitem import CartItem
from models.menu import Menu
from models.restaurant import Restaurant
from models.cookingstatus import CookingStatus
from models.faq import FAQ
from models.incentive import Incentive
from models.order import Order
from models.orderitem import OrderItem
from models.pooling_order import PoolingOrder
from models.referral import Referral
from models.user_setting import UserSettings
from models.wallet_transaction import WalletTransaction
from models.wallet import Wallet
from models.promocode import PromoCode
from models.shop import Shop
from models.cooking_dish import CookingDish
from models.unit import DishUnit
from models.type import Type
from models.timings import Timing
from models.delivery_incentive import DeliveryIncentive
from models.location import UserLocation


Base.metadata.create_all(bind=engine)
print("All tables created")