from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database.db import get_db
from models.shop import Shop
from database.shop import ShopCreate, ShopUpdate

router = APIRouter(prefix="/shop", tags=["Shop Profile"])

# -------------------------------------------Create----------------------
# @router.post("/create")
# def create_shop(
#     payload: ShopCreate,
#     owner_id: int,
#     db: Session = Depends(get_db)
# ):
#     existing = db.query(Shop).filter(Shop.owner_id == owner_id).first()
#     if existing:
#         raise HTTPException(400, "Shop profile already exists")

#     shop = Shop(owner_id=owner_id, **payload.dict())
#     db.add(shop)
#     db.commit()
#     db.refresh(shop)

#     return {
#         "message": "Shop profile created",
#         "shop_id": shop.id
#     }

# # --------------------------------GET--------------------------------------------

# @router.get("/{owner_id}")
# def get_shop(owner_id: int, db: Session = Depends(get_db)):
#     shop = db.query(Shop).filter(Shop.owner_id == owner_id).first()
#     if not shop:
#         raise HTTPException(404, "Shop profile not found")

#     return shop


@router.post("/create")
def create_shop(
    payload: ShopCreate,
    owner_id: int,
    db: Session = Depends(get_db)
):
    existing = db.query(Shop).filter(Shop.owner_id == owner_id).first()
    if existing:
        raise HTTPException(400, "Shop profile already exists")

    shop = Shop(
        owner_id=owner_id,
        status="pending",
        **payload.dict()
    )

    db.add(shop)
    db.commit()
    db.refresh(shop)

    return {
        "message": "Shop profile created. Waiting for admin approval",
        "shop_id": shop.id,
        "status": shop.status
    }




# ------------------------------------------UPDATE-----------------------------

@router.put("/{owner_id}")
def update_shop_profile(
    owner_id: int,
    shop_name: Optional[str] = None,
    address: Optional[str] = None,
    certificate_no: Optional[str] = None,
    gst_number: Optional[str] = None,
    bank_name: Optional[str] = None,
    account_number: Optional[str] = None,
    IFSC_Code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    shop = db.query(Shop).filter(Shop.owner_id == owner_id).first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

   
    if shop_name is not None:
        shop.shop_name = shop_name

    if address is not None:
        shop.address = address

    if certificate_no is not None:
        shop.certificate_no = certificate_no

    if gst_number is not None:
        shop.gst_number = gst_number

    if bank_name is not None:
        shop.bank_name = bank_name

    if account_number is not None:
        shop.account_number = account_number

    if IFSC_Code is not None:
        shop.IFSC_Code = IFSC_Code.upper()

    db.commit()
    db.refresh(shop)

    return {
        "message": "Shop profile updated successfully",
        "data": {
            "id": shop.id,
            "owner_id": shop.owner_id,
            "shop_name": shop.shop_name,
            "address": shop.address,
            "certificate_no": shop.certificate_no,
            "gst_number": shop.gst_number,
            "bank_name": shop.bank_name,
            "account_number": shop.account_number,
            "IFSC_Code": shop.IFSC_Code
        }
    }


# --------------------------------------STATUS---------------------------------------------


@router.get("/admin/pending")
def get_pending_shops(db: Session = Depends(get_db)):

    shops = db.query(Shop).filter(Shop.status == "pending").all()

    if not shops:
        raise HTTPException(404, "No pending shop approvals")

    return shops



# ----------------------------------APPROVE------------------------------------------------


@router.put("/admin/approve/{shop_id}")
def approve_shop(shop_id: int, db: Session = Depends(get_db)):

    shop = db.query(Shop).filter(Shop.id == shop_id).first()

    if not shop:
        raise HTTPException(404, "Shop not found")

    shop.status = "approved"

    db.commit()
    db.refresh(shop)

    return {
        "message": "Shop approved successfully",
        "shop_id": shop.id,
        "status": shop.status
    }




