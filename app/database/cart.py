from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.cart import Cart
from models.cartitem import CartItem
from models.menu import Menu

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()