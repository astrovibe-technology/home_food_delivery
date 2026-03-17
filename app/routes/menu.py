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
    description: str
    dish_type: str   # society / travel
    food_type: str   # veg / non_veg

class BulkMenuCreate(BaseModel):
    menus: List[MenuCreate]



@router.post("/menus/bulk-create")
def bulk_create_menu(
    shop_id: int,
    request: BulkMenuCreate,
    db: Session = Depends(get_db)
):

    created_items = []

    for item in request.menus:

        menu = Menu(
            shop_id=shop_id,
            name=item.name,
            description=item.description,
            price=item.price,
            dish_type=item.dish_type.lower(),
            food_type=item.food_type.lower()
        )

        db.add(menu)

        created_items.append({
            "name": item.name,
            "dish_type": item.dish_type,
            "food_type": item.food_type
        })

    db.commit()

    return {
        "message": "Menus created successfully",
        "total": len(created_items),
        "items": created_items
    }



@router.get("/by-shop")
def get_menus_by_shop(
    shop_id: int,
    dish_type: str = None,  
    db: Session = Depends(get_db)
):

    # Check shop exists
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    query = db.query(Menu).filter(Menu.shop_id == shop_id)

    # Apply filter only if provided
    if dish_type:
        query = query.filter(Menu.dish_type == dish_type.lower())

    menus = query.all()

    if not menus:
        return {
            "shop_id": shop_id,
            "menus": [],
            "message": "No menus found"
        }

    menu_list = []
    for menu in menus:
        menu_list.append({
            "menu_id": menu.id,
            "name": menu.name,
            "price": menu.price,
            "description": menu.description,
            "dish_type": menu.dish_type,
            "food_type": menu.food_type
        })

    return {
        "shop_id": shop_id,
        "total_menus": len(menu_list),
        "menus": menu_list
    }