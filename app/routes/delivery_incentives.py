from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.db import get_db
from models.delivery_incentive import DeliveryIncentive

router = APIRouter(prefix="/delivery_incentive", tags=["Delivery Incentive"])


# 🔥 UPDATE INCENTIVE FUNCTION
def update_incentive(db, user_id):

    print("🔥 INCENTIVE CALLED FOR USER:", user_id)

    today = datetime.utcnow().date()

    # ✅ Week start (Monday)
    week_start = today - timedelta(days=today.weekday())

    month = today.month
    year = today.year

    # ✅ Check existing record
    inc = db.query(DeliveryIncentive).filter(
        DeliveryIncentive.user_id == user_id,
        DeliveryIncentive.week_start == week_start,
        DeliveryIncentive.month == month,
        DeliveryIncentive.year == year
    ).first()

    # ✅ Create new record if not exists
    if not inc:
        inc = DeliveryIncentive(
            user_id=user_id,
            week_start=week_start,
            month=month,
            year=year,
            week_orders=0,
            month_orders=0,
            lifetime_orders=0
        )
        db.add(inc)
        db.commit()
        db.refresh(inc)

    # 🔥 RESET LOGIC
    if inc.week_start != week_start:
        inc.week_orders = 0
        inc.week_start = week_start

    if inc.month != month:
        inc.month_orders = 0
        inc.month = month

    # ✅ Increment counts
    inc.week_orders += 1
    inc.month_orders += 1
    inc.lifetime_orders += 1

    db.commit()


# 🔥 GET INCENTIVE API (UPDATED WITH REWARD AMOUNT)
@router.get("/incentive/{user_id}")
def get_incentive(user_id: int, db: Session = Depends(get_db)):

    inc = db.query(DeliveryIncentive).filter(
        DeliveryIncentive.user_id == user_id
    ).order_by(DeliveryIncentive.id.desc()).first()

    if not inc:
        return {"message": "No incentive data"}

    # ✅ Reward Logic
    weekly_reward = "₹100 Earned" if inc.week_orders >= 40 else "₹0"
    monthly_reward = "₹500 Earned" if inc.month_orders >= 160 else "₹0"
    lifetime_reward = "₹1,00,000 Earned" if inc.lifetime_orders >= 40000 else "In progress"

    lifetime_goal = 40000

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
            "progress": f"{inc.lifetime_orders} / {lifetime_goal}",
            "remaining": lifetime_goal - inc.lifetime_orders,
            "reward": lifetime_reward
        }
    }