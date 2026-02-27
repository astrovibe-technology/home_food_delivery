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

   
    if not units:
        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )

    return units




from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

@router.put("/{unit_id}")
def update_unit(
    unit_id: int,
    unit_type: Optional[str] = None,
    measurement: Optional[str] = None,
    quantity: Optional[int] = None,
    db: Session = Depends(get_db)
):
    unit = db.query(DishUnit).filter(DishUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Update only if provided
    if unit_type is not None:
        unit.unit_type = unit_type.upper()

    if measurement is not None:
        unit.measurement = measurement

    if quantity is not None:
        unit.quantity = quantity

    db.commit()
    db.refresh(unit)

    return {
        "message": "Unit updated successfully",
        "data": {
            "id": unit.id,
            "unit_type": unit.unit_type,
            "measurement": unit.measurement,
            "quantity": unit.quantity
        }
    }




@router.delete("/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(DishUnit).filter(DishUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    db.delete(unit)
    db.commit()

    return {"message": "Unit deleted successfully"}

