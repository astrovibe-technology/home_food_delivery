from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from database.db import SessionLocal
from models.menu import Menu
from models.user import User
from models.shop import Shop   

router = APIRouter(prefix="/menus", tags=["Menu"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/add")
# def add_menu(
#     user_id: int,
#     shop_id: int,
#     name: str,
#     price: int,
#     description: str = None,
#     db: Session = Depends(get_db)
# ):

#     # check user
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # check shop
#     shop = db.query(Shop).filter(Shop.id == shop_id).first()
#     if not shop:
#         raise HTTPException(status_code=404, detail="Shop not found")

#     menu = Menu(
#         name=name,
#         price=price,
#         description=description,
#         is_available=True,
#         created_by=user_id,
#         shop_id=shop_id
#     )

#     db.add(menu)
#     db.commit()
#     db.refresh(menu)

#     return {
#         "message": "Menu added successfully",
#         "menu_id": menu.id,
#         "shop_id": shop_id,
#         "created_by": user_id
#     }

class MenuCreate(BaseModel):
    name: str
    price: int
    description: Optional[str] = None


@router.post("/bulk-create")
def create_multiple_menus(
    shop_id: int,
    menus: List[MenuCreate],
    db: Session = Depends(get_db)
):

    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    response_items = {}

    for index, menu_data in enumerate(menus, start=1):

        menu = Menu(
            name=menu_data.name,
            price=menu_data.price,
            description=menu_data.description,
            shop_id=shop_id,
            is_available=True
        )

        db.add(menu)
        db.commit()
        db.refresh(menu)

        response_items[f"item{index}"] = {
            "menu_id": menu.id,
            "name": menu.name,
            "price": menu.price,
            "description": menu.description
        }

    return {
        "message": "Menus created successfully",
        "total_items": len(menus),
        "menus": response_items
    }



@router.get("/by-shop")
def get_menus_by_shop(
    shop_id: int,
    db: Session = Depends(get_db)
):
    # Check shop exists
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    menus = db.query(Menu).filter(Menu.shop_id == shop_id).all()

    if not menus:
        return {
            "shop_id": shop_id,
            "menus": [],
            "message": "No menus found for this shop"
        }

    menu_list = []
    for menu in menus:
        menu_list.append({
            "menu_id": menu.id,
            "name": menu.name,
            "price": menu.price,
            "description": menu.description,
            # "is_available": menu.is_available
        })

    return {
        "shop_id": shop_id,
        "total_menus": len(menu_list),
        "menus": menu_list
    }