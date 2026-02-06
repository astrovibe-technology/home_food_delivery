from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.db import get_db
from models.delivery_incentive import DeliveryIncentive


router = APIRouter(prefix="/delivery_incentive", tags=["delivery_incentive"])


def update_incentive(db, user_id):

    today = datetime.utcnow().date()

    # Get Monday (week start)
    week_start = today - timedelta(days=today.weekday())

    # Get month/year
    month = today.month
    year = today.year

    inc = db.query(DeliveryIncentive).filter(
        DeliveryIncentive.user_id == user_id,
        DeliveryIncentive.week_start == week_start,
        DeliveryIncentive.month == month,
        DeliveryIncentive.year == year
    ).first()

    if not inc:
        inc = DeliveryIncentive(
            user_id=user_id,
            week_start=week_start,
            month=month,
            year=year
        )
        db.add(inc)

    # Increase counts
    inc.week_orders += 1
    inc.month_orders += 1
    inc.lifetime_orders += 1

    db.commit()




@router.get("/incentive/{user_id}")
def get_incentive(user_id: int, db: Session = Depends(get_db)):

    inc = db.query(DeliveryIncentive).filter(
        DeliveryIncentive.user_id == user_id
    ).order_by(DeliveryIncentive.id.desc()).first()

    if not inc:
        return {"message": "No incentive data"}

    # Weekly reward
    weekly_reward = 100 if inc.week_orders >= 40 else 0

    # Monthly reward
    monthly_reward = 500 if inc.month_orders >= 160 else 0

    # Lifetime progress
    lifetime_goal = 40000
    lifetime_progress = inc.lifetime_orders

    return {
        "weekly": {
            "orders": inc.week_orders,
            "goal": 40,
            "reward": weekly_reward,
            "achieved": inc.week_orders >= 40
        },
        "monthly": {
            "orders": inc.month_orders,
            "goal": 160,
            "reward": monthly_reward,
            "achieved": inc.month_orders >= 160
        },
        "lifetime": {
            "progress": f"{lifetime_progress} / {lifetime_goal}",
            "remaining": lifetime_goal - lifetime_progress,
            "reward": "Hamper worth ₹1,00,000" if lifetime_progress >= lifetime_goal else "In progress"
        }
    }