from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.menu import Menu

router = APIRouter(prefix="/menus", tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_menu(
    # restaurant_id: int,
    name: str,
    price: int,
    description: str = None,
    db: Session = Depends(get_db)
):
    menu = Menu(
        # restaurant_id=restaurant_id,
        name=name,
        price=price,
        description=description,
        is_available=True
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)

    return {
        "message": "Menu added successfully",
        "menu_id": menu.id
    }