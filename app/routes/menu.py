from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.menu import Menu
from models.user import User

router = APIRouter(prefix="/menus", tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_menu(
    user_id: int,  
    name: str,
    price: int,
    description: str = None,
    db: Session = Depends(get_db)
):

   
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    menu = Menu(
        name=name,
        price=price,
        description=description,
        is_available=True,
        created_by=user_id  
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)

    return {
        "message": "Menu added successfully",
        "menu_id": menu.id,
        "created_by": user_id
    }