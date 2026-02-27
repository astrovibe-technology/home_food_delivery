from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database.db import get_db
from models.type import Type
from sqlalchemy import or_

router = APIRouter(prefix="/type", tags=["Type"])



@router.post("/")
def create_type(
    name: str,
    is_active: bool = True,   
    db: Session = Depends(get_db)
):
    existing = db.query(Type).filter(
        Type.name == name.upper()
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Type already exists"
        )

    type_obj = Type(
        name=name.upper(),
        is_active=is_active
    )

    db.add(type_obj)
    db.commit()
    db.refresh(type_obj)

    return {
        "message": "Type created successfully",
        "id": type_obj.id,
        "name": type_obj.name,
        "is_active": type_obj.is_active
    }



@router.get("/")
def get_types(db: Session = Depends(get_db)):
    types = db.query(Type).filter(
        or_(
            Type.is_active == True,
            Type.is_active == None
        )
    ).all()

   
    if not types:
        raise HTTPException(
            status_code=404,
            detail="No data found"
        )

    return types



@router.put("/{type_id}")
def update_type(
    type_id: int,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    type_obj = db.query(Type).filter(Type.id == type_id).first()

    if not type_obj:
        raise HTTPException(status_code=404, detail="Type not found")

    # ✅ If name provided → check duplicate
    if name is not None:
        existing = db.query(Type).filter(
            Type.name == name.upper(),
            Type.id != type_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Type name already exists"
            )

        type_obj.name = name.upper()

    # ✅ If is_active provided → update
    if is_active is not None:
        type_obj.is_active = is_active

    # ❗ Optional: If nothing provided
    if name is None and is_active is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field (name or is_active) must be provided"
        )

    db.commit()
    db.refresh(type_obj)

    return {
        "message": "Type updated successfully",
        "id": type_obj.id,
        "name": type_obj.name,
        "is_active": type_obj.is_active
    }



@router.delete("/{type_id}")
def delete_type(type_id: int, db: Session = Depends(get_db)):
    type_obj = db.query(Type).filter(Type.id == type_id).first()
    
    if not type_obj:
        raise HTTPException(status_code=404, detail="Type not found")
    
    db.delete(type_obj) 
    db.commit()
    
    return {
        "message": "Type deleted successfully",
        "id": type_id,
        "name": type_obj.name
    }


