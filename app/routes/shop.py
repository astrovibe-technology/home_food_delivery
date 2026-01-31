from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.shop import Shop
from database.shop import ShopCreate, ShopUpdate

router = APIRouter(prefix="/shop", tags=["Shop Profile"])

# -------------------------------------------Create----------------------
@router.post("/create")
def create_shop(
    payload: ShopCreate,
    owner_id: int,
    db: Session = Depends(get_db)
):
    existing = db.query(Shop).filter(Shop.owner_id == owner_id).first()
    if existing:
        raise HTTPException(400, "Shop profile already exists")

    shop = Shop(owner_id=owner_id, **payload.dict())
    db.add(shop)
    db.commit()
    db.refresh(shop)

    return {
        "message": "Shop profile created",
        "shop_id": shop.id
    }

# --------------------------------GET--------------------------------------------

@router.get("/{owner_id}")
def get_shop(owner_id: int, db: Session = Depends(get_db)):
    shop = db.query(Shop).filter(Shop.owner_id == owner_id).first()
    if not shop:
        raise HTTPException(404, "Shop profile not found")

    return shop

# ------------------------------------------UPDATE-----------------------------

@router.put("/update/{owner_id}")
def update_shop(
    owner_id: int,
    payload: ShopUpdate,
    db: Session = Depends(get_db)
):
    shop = db.query(Shop).filter(Shop.owner_id == owner_id).first()
    if not shop:
        raise HTTPException(404, "Shop profile not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(shop, key, value)

    db.commit()

    return {"message": "Shop profile updated"}




