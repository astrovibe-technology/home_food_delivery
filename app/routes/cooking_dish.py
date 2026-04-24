from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
import shutil, os, uuid
from datetime import datetime
from models.menu import Menu
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

    # ✅ diet tags
    is_sugar_free: bool = Form(False),
    is_spicy: bool = Form(False),

    description: str = Form(...),
    price: int = Form(...),
    delivery_datetime: str = Form(...),
    last_order_time: str = Form(...),

    address_line: str = Form(...),
    landmark: str = Form(None),
    area_name: str = Form(...),
    pincode: str = Form(...),

    halal_certificate: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    # ✅ shop check
    shop = check_shop_approved(db, user_id)

    certificate_path = None

    # ✅ EXACT SAME AS TRAVEL
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

    # ✅ datetime
    delivery_dt = parse_datetime(delivery_datetime)
    last_order_dt = parse_datetime(last_order_time)

    # ✅ diet_tags
    tags = []
    if is_sugar_free:
        tags.append("SUGAR_FREE")
    if is_spicy:
        tags.append("SPICY")

    diet_tags = ",".join(tags) if tags else None

    # ✅ save
    dish = CookingDish(
        user_id=user_id,
        restaurant_id=shop.id,
        title=title,
        food_type=food_type,
        is_halal=is_halal,
        halal_certificate=certificate_path,
        description=description,
        price=price,
        delivery_datetime=delivery_dt,
        last_order_time=last_order_dt,
        diet_tags=diet_tags,
        address_line=address_line,
        landmark=landmark,
        area_name=area_name,
        pincode=pincode,
        dish_type="SOCIETY",
        is_published=True
    )

    db.add(dish)
    db.commit()
    db.refresh(dish)

    return {
        "message": "Dish published successfully",
        "dish_id": dish.id,
        "diet_tags": dish.diet_tags
    }



@router.get("/society")
def get_society_dishes(db: Session = Depends(get_db)):

    dishes = db.query(CookingDish).filter(
        CookingDish.dish_type == "SOCIETY"
    ).order_by(CookingDish.id.desc()).all()

    result = []

    for dish in dishes:

        # ✅ split diet_tags
        tags = dish.diet_tags.split(",") if dish.diet_tags else []

        result.append({
            "dish_id": dish.id,
            "user_id": dish.user_id,
            "restaurant_id": dish.restaurant_id,
            "title": dish.title,
            "food_type": dish.food_type,
            "is_halal": dish.is_halal,
            "description": dish.description,
            "price": dish.price,
            "delivery_datetime": dish.delivery_datetime,
            "last_order_time": dish.last_order_time,

            # ✅ diet fields
            "is_sugar_free": "SUGAR_FREE" in tags,
            "is_spicy": "SPICY" in tags,
            "diet_tags": tags,   # optional (list ah return)

            # location
            "address_line": dish.address_line,
            "landmark": dish.landmark,
            "area_name": dish.area_name,
            "pincode": dish.pincode,

            "dish_type": dish.dish_type
        })

    return {
        "total_dishes": len(result),
        "dishes": result
    }


@router.get("/shop/{shop_id}")
def get_all_shop_items(
    shop_id: int,
    db: Session = Depends(get_db)
):

    cooking_dishes = db.query(CookingDish).filter(
        CookingDish.restaurant_id == shop_id
    ).all()

    menus = db.query(Menu).filter(
        Menu.shop_id == shop_id
    ).all()

    result = []

    # Cooking dishes
    for dish in cooking_dishes:
        result.append({
            "id": dish.id,
            "title": dish.title,
            "price": dish.price,
            "description": dish.description,
            "type": dish.dish_type
        })

    # Menu dishes
    for menu in menus:
        result.append({
            "id": menu.id,
            "title": menu.name,
            "price": menu.price,
            "description": menu.description,
            "type": "RESTAURANT"
        })

    return {
        "shop_id": shop_id,
        "total_items": len(result),
        "items": result
    }


# -------------------------------- TRAVEL --------------------------------

@router.post("/travel")
def create_travel_dish(
    user_id: int = Form(...),

    title: str = Form(...),
    food_type: str = Form(...),
    is_halal: bool = Form(False),

    # ✅ NEW (only this added)
    is_sugar_free: bool = Form(False),
    is_spicy: bool = Form(False),

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

    # ✅ (UNCHANGED halal validation)
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

    # ✅ datetime
    delivery_dt = parse_datetime(delivery_datetime)
    last_order_dt = parse_datetime(last_order_time)

    travel_type = travel_type.upper()

    # ✅ travel validations
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

    # ✅ NEW (diet_tags மட்டும்)
    tags = []
    if is_sugar_free:
        tags.append("SUGAR_FREE")
    if is_spicy:
        tags.append("SPICY")

    diet_tags = ",".join(tags) if tags else None

    # ✅ save
    dish = CookingDish(
        user_id=user_id,
        restaurant_id=shop.id,
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

        # ✅ ONLY THIS NEW FIELD
        diet_tags=diet_tags,

        dish_type="TRAVEL",
        is_published=True
    )

    db.add(dish)
    db.commit()
    db.refresh(dish)

    return {
        "message": "Travel dish published successfully",
        "dish_id": dish.id,
        "diet_tags": dish.diet_tags
    }




@router.get("/travel/get-all-travel-dishes")
def get_all_travel_dishes(db: Session = Depends(get_db)):

    dishes = db.query(CookingDish).filter(
        CookingDish.dish_type == "TRAVEL"
    ).order_by(CookingDish.id.desc()).all()

    result = []

    for dish in dishes:

        # ✅ split diet_tags
        tags = dish.diet_tags.split(",") if dish.diet_tags else []

        result.append({
            "id": dish.id,
            "user_id": dish.user_id,
            "restaurant_id": dish.restaurant_id,
            "title": dish.title,
            "food_type": dish.food_type,
            "is_halal": dish.is_halal,
            "description": dish.description,
            "price": dish.price,
            "delivery_datetime": dish.delivery_datetime,
            "last_order_time": dish.last_order_time,

            # ✅ diet fields (NEW)
            "is_sugar_free": "SUGAR_FREE" in tags,
            "is_spicy": "SPICY" in tags,
            "diet_tags": tags,   # optional

            # Travel fields
            "travel_type": dish.travel_type,
            "train_name": dish.train_name,
            "train_number": dish.train_number,
            "bus_number": dish.bus_number,
            "route": dish.route,
            "bogie_number": dish.bogie_number,
            "seat_number": dish.seat_number,

            "dish_type": dish.dish_type
        })

    return {
        "total_dishes": len(result),
        "dishes": result
    }





@router.get("/travel/{shop_id}")
def get_travel_shop_items(
    shop_id: int,
    db: Session = Depends(get_db)
):

    cooking_dishes = db.query(CookingDish).filter(
        CookingDish.restaurant_id == shop_id,
        CookingDish.dish_type == "TRAVEL"
    ).all()

    menus = db.query(Menu).filter(
        Menu.shop_id == shop_id
    ).all()

    result = []

    # Travel cooking dishes
    for dish in cooking_dishes:
        result.append({
            "id": dish.id,
            "title": dish.title,
            "price": dish.price,
            "description": dish.description,
            "type": dish.dish_type
        })

    # Menu dishes
    for menu in menus:
        result.append({
            "id": menu.id,
            "title": menu.name,
            "price": menu.price,
            "description": menu.description,
            "type": "RESTAURANT"
        })

    return {
        "shop_id": shop_id,
        "total_items": len(result),
        "items": result
    }



@router.get("/search")
def search_dishes(
    area_name: str = None,
    pincode: str = None,
    address_line: str = None,   # ✅ NEW
    train_number: str = None,
    db: Session = Depends(get_db)
):

    # ---------------- TRAVEL SEARCH ----------------
    if train_number:

        travel_query = db.query(CookingDish).filter(
            CookingDish.dish_type == "TRAVEL",
            CookingDish.train_number == train_number
        )

        travel_dishes = travel_query.all()

        if not travel_dishes:
            raise HTTPException(
                status_code=404,
                detail="No travel data found for given train number"
            )

        result = []
        for dish in travel_dishes:

            shop = db.query(Shop).filter(Shop.id == dish.restaurant_id).first()

            result.append({
                "id": dish.id,
                "type": "TRAVEL",
                "title": dish.title,
                "price": dish.price,
                "train_name": dish.train_name,
                "train_number": dish.train_number,
                "route": dish.route,

                # ✅ ADD
                "kitchen_id": dish.restaurant_id,
                "kitchen_name": shop.shop_name if shop else None
            })

        return {
            "type": "TRAVEL",
            "total": len(result),
            "data": result
        }

    # ---------------- SOCIETY SEARCH ----------------
    elif area_name or pincode or address_line:

        society_query = db.query(CookingDish).filter(
            CookingDish.dish_type == "SOCIETY"
        )

        if area_name:
            society_query = society_query.filter(
                CookingDish.area_name.ilike(f"%{area_name}%")
            )

        if pincode:
            society_query = society_query.filter(
                CookingDish.pincode == pincode
            )

        # ✅ NEW FILTER
        if address_line:
            society_query = society_query.filter(
                CookingDish.address_line.ilike(f"%{address_line}%")
            )

        society_dishes = society_query.all()

        if not society_dishes:
            raise HTTPException(
                status_code=404,
                detail="No society data found"
            )

        result = []
        for dish in society_dishes:

            shop = db.query(Shop).filter(Shop.id == dish.restaurant_id).first()

            result.append({
                "id": dish.id,
                "type": "SOCIETY",
                "title": dish.title,
                "price": dish.price,
                "area_name": dish.area_name,
                "pincode": dish.pincode,
                "address_line": dish.address_line,
                "landmark": dish.landmark,

                # ✅ ADD
                "kitchen_id": dish.restaurant_id,
                "kitchen_name": shop.shop_name if shop else None
            })

        return {
            "type": "SOCIETY",
            "total": len(result),
            "data": result
        }

    # ---------------- INVALID INPUT ----------------
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide area_name or pincode or address_line or train_number"
        )