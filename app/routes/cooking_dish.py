from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
import shutil, os, uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database.db import get_db
from models.cooking_dish import CookingDish

router = APIRouter(prefix="/cooking", tags=["Cooking"])

UPLOAD_DIR = "app/uploads/halal_certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/society")
def create_society_dish(
    title: str = Form(...),
    food_type: str = Form(...),  # VEG / NON_VEG
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
    certificate_path = None

    # ✅ Validation
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

    dish = CookingDish(
        title=title,
        food_type=food_type,
        is_halal=is_halal,
        halal_certificate=certificate_path,
        description=description,
        price=price,
        delivery_datetime=delivery_datetime,
        last_order_time=last_order_time,
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


# ----------------------------------------------------TRAVEL-------------------------------------------


@router.post("/travel")
def create_travel_dish(
    title: str = Form(...),
    food_type: str = Form(...),  # VEG / NON_VEG
    is_halal: bool = Form(False),
    description: str = Form(...),
    price: int = Form(...),
    delivery_datetime: str = Form(...),
    last_order_time: str = Form(...),

    travel_type: str = Form(...),  # TRAIN / BUS
    train_name: str = Form(None),
    train_number: str = Form(None),
    bus_number: str = Form(None),
    route: str = Form(...),
    bogie_number: str = Form(None),
    seat_number: str = Form(None),

    halal_certificate: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    certificate_path = None

    # ✅ If halal is True, certificate is required
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

    # Convert string datetime to datetime objects
    try:
        delivery_dt = datetime.fromisoformat(delivery_datetime)
        last_order_dt = datetime.fromisoformat(last_order_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format, use ISO format")

    dish = CookingDish(
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