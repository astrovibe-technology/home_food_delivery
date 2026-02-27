from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.timings import Timing
from datetime import datetime,time

router = APIRouter(prefix="/timing", tags=["Timing"])

# -----------------------
# CREATE timing
# -----------------------
@router.post("/")
def create_timing(
    name: str,
    start_time: str, 
    end_time: str,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    
    existing = db.query(Timing).filter(Timing.name == name.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Timing with this name already exists")

    try:
        start = datetime.strptime(start_time, "%H:%M").time()
        end = datetime.strptime(end_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Time must be in HH:MM format (24-hour)")

    timing = Timing(
        name=name.upper(),
        start_time=start,
        end_time=end,
        is_active=is_active
    )
    db.add(timing)
    db.commit()
    db.refresh(timing)
    return {
        "message": "Timing created successfully",
        "timing_id": timing.id,
        "is_active": timing.is_active
    }

# -----------------------
# GET all timings
# -----------------------
@router.get("/")
def get_timings(db: Session = Depends(get_db)):
    timings = db.query(Timing).all()

    
    if not timings:
        raise HTTPException(
            status_code=404,
            detail="No data found"
        )

    return [
        {
            "id": t.id,
            "name": t.name,
            "start_time": t.start_time.strftime("%H:%M"),
            "end_time": t.end_time.strftime("%H:%M"),
            "is_active": t.is_active
        }
        for t in timings
    ]

# -----------------------
# UPDATE timing
# -----------------------
@router.put("/{timing_id}")
def update_timing(
    timing_id: int,
    start_time: str = None,  # "HH:MM"
    end_time: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    timing = db.query(Timing).filter(Timing.id == timing_id).first()
    if not timing:
        raise HTTPException(status_code=404, detail="Timing not found")

    # Convert times safely
    if start_time:
        try:
            timing.start_time = datetime.strptime(start_time, "%H:%M").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Start time must be in HH:MM format")
    if end_time:
        try:
            timing.end_time = datetime.strptime(end_time, "%H:%M").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="End time must be in HH:MM format")

    if is_active is not None:
        timing.is_active = is_active

    db.commit()
    db.refresh(timing)

    return {
        "message": "Timing updated successfully",
        "timing_id": timing.id,
        "is_active": timing.is_active
    }

# -----------------------
# DELETE timing (deactivate)
# -----------------------
@router.delete("/{timing_id}")
def delete_timing(timing_id: int, db: Session = Depends(get_db)):
    timing = db.query(Timing).filter(Timing.id == timing_id).first()
    if not timing:
        raise HTTPException(status_code=404, detail="Timing not found")

 
    db.delete(timing)
    db.commit()

    return {"message": "Timing deleted successfully"}