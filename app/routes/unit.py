from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.unit import DishUnit

router = APIRouter(prefix="/units", tags=["Dish Units"])


@router.post("/add")
def add_unit(
    unit_type: str,
    measurement: str,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    unit = DishUnit(
        unit_type=unit_type.upper(),
        measurement=measurement,
        quantity=quantity
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)

    return {
        "message": "Unit added successfully",
        "unit_id": unit.id
    }



@router.get("/")
def get_units(db: Session = Depends(get_db)):
    units = db.query(DishUnit).all()
    return units




@router.put("/{unit_id}")
def update_unit(
    unit_id: int,
    unit_type: str,
    measurement: str,
    quantity: int,
    db: Session = Depends(get_db)
):
    unit = db.query(DishUnit).filter(DishUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit.unit_type = unit_type.upper()
    unit.measurement = measurement
    unit.quantity = quantity

    db.commit()

    return {"message": "Unit updated successfully"}




@router.delete("/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(DishUnit).filter(DishUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    db.delete(unit)
    db.commit()

    return {"message": "Unit deleted successfully"}

