from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
import shutil, os, uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database.db import get_db
from models.cooking_dish import CookingDish
from models.shop import Shop

router = APIRouter(prefix="/cooking", tags=["Cooking"])

UPLOAD_DIR = "app/uploads/halal_certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------- SHOP APPROVAL CHECK ----------------------

def check_shop_approved(db: Session, user_id: int):

    shop = db.query(Shop).filter(Shop.owner_id == user_id).first()

    if not shop:
        raise HTTPException(
            status_code=404,
            detail="Shop profile not found"
        )

    if shop.status != "approved":
        raise HTTPException(
            status_code=403,
            detail="Shop not approved by admin. Cannot create dish"
        )

    return shop


# -------------------------- DATETIME PARSER --------------------------

def parse_datetime(value: str):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise HTTPException(
        status_code=400,
        detail="Invalid datetime format. Use YYYY-MM-DD HH:MM or YYYY-MM-DD HH:MM:SS"
    )


# -------------------------------- SOCIETY --------------------------------

@router.post("/society")
def create_society_dish(
    user_id: int = Form(...),

    title: str = Form(...),
    food_type: str = Form(...),
    is_halal: bool = Form(False),
    description: str = Form(...),
    price: int = Form(...),
    delivery_datetime: str = Form(...),
    last_order_time: str = Form(...),

    building_name: str = Form(...),
    house_number: str = Form(...),
    floor_number: str = Form(...),

    halal_certificate: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    # ✅ shop check
    shop = check_shop_approved(db, user_id)

    certificate_path = None

    if food_type == "NON_VEG" and is_halal:
        if not halal_certificate:
            raise HTTPException(
                status_code=400,
                detail="Halal certificate image is required"
            )

        ext = halal_certificate.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(halal_certificate.file, buffer)

        certificate_path = file_path

    delivery_dt = parse_datetime(delivery_datetime)
    last_order_dt = parse_datetime(last_order_time)

    dish = CookingDish(
        user_id=user_id,
        restaurant_id=shop.id,   # ✅ IMPORTANT CHANGE
        title=title,
        food_type=food_type,
        is_halal=is_halal,
        halal_certificate=certificate_path,
        description=description,
        price=price,
        delivery_datetime=delivery_dt,
        last_order_time=last_order_dt,
        building_name=building_name,
        house_number=house_number,
        floor_number=floor_number,
        dish_type="SOCIETY",
        is_published=True
    )

    db.add(dish)
    db.commit()
    db.refresh(dish)

    return {
        "message": "Dish published successfully",
        "dish_id": dish.id
    }


# -------------------------------- TRAVEL --------------------------------

@router.post("/travel")
def create_travel_dish(
    user_id: int = Form(...),

    title: str = Form(...),
    food_type: str = Form(...),
    is_halal: bool = Form(False),
    description: str = Form(...),
    price: int = Form(...),

    delivery_datetime: str = Form(...),
    last_order_time: str = Form(...),

    travel_type: str = Form(...),
    train_name: str = Form(None),
    train_number: str = Form(None),
    bus_number: str = Form(None),
    route: str = Form(...),
    bogie_number: str = Form(None),
    seat_number: str = Form(None),

    halal_certificate: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    # ✅ shop check
    shop = check_shop_approved(db, user_id)

    certificate_path = None

    delivery_dt = parse_datetime(delivery_datetime)
    last_order_dt = parse_datetime(last_order_time)

    if last_order_dt >= delivery_dt:
        raise HTTPException(
            status_code=400,
            detail="Last order time must be before delivery time"
        )

    if delivery_dt <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Delivery datetime must be in the future"
        )

    if is_halal:
        if not halal_certificate:
            raise HTTPException(
                status_code=400,
                detail="Halal certificate image is required for halal dishes"
            )

        ext = halal_certificate.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(halal_certificate.file, buffer)

        certificate_path = file_path

    travel_type = travel_type.upper()

    if travel_type == "TRAIN":
        if not train_name or not train_number:
            raise HTTPException(
                status_code=400,
                detail="Train name and train number required for TRAIN"
            )

    if travel_type == "BUS":
        if not bus_number:
            raise HTTPException(
                status_code=400,
                detail="Bus number required for BUS"
            )

    dish = CookingDish(
        user_id=user_id,
        restaurant_id=shop.id,   # ✅ IMPORTANT CHANGE
        title=title,
        food_type=food_type,
        is_halal=is_halal,
        halal_certificate=certificate_path,
        description=description,
        price=price,
        delivery_datetime=delivery_dt,
        last_order_time=last_order_dt,
        travel_type=travel_type,
        train_name=train_name,
        train_number=train_number,
        bus_number=bus_number,
        route=route,
        bogie_number=bogie_number,
        seat_number=seat_number,
        dish_type="TRAVEL",
        is_published=True
    )

    db.add(dish)
    db.commit()
    db.refresh(dish)

    return {
        "message": "Travel dish published successfully",
        "dish_id": dish.id
    }