from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random, string

from database.db import get_db
from models.user import User
from models.referral import Referral

router = APIRouter(prefix="/referral", tags=["Referral"])


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.get("/links/{user_id}")
def get_referral_links(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.referral_code:
        user.referral_code = generate_referral_code()
        db.commit()

    android_link = f"https://yourapp.com/android?ref={user.referral_code}"
    ios_link = f"https://yourapp.com/ios?ref={user.referral_code}"

    return {
        "android_referral_link": android_link,
        "ios_referral_link": ios_link
    }



@router.post("/apply")
def apply_referral(
    new_user_id: int,
    referral_code: str,
    db: Session = Depends(get_db)
):
    # 🔍 Check referral code
    referrer = db.query(User).filter(
        User.referral_code == referral_code
    ).first()

    if not referrer:
        raise HTTPException(
            status_code=400,
            detail="Invalid referral code"
        )

    # 🔍 Check new user
    new_user = db.query(User).filter(
        User.id == new_user_id
    ).first()

    if not new_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 🚫 Prevent self referral
    if referrer.id == new_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot refer yourself"
        )

    # 🚫 Prevent multiple referrals
    if new_user.referred_by:
        raise HTTPException(
            status_code=400,
            detail="Referral already applied"
        )

    # ✅ Apply referral
    new_user.referred_by = referrer.id
    db.commit()

    return {
        "message": "Referral applied successfully"
    }




@router.get("/dashboard/{user_id}")
def referral_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    completed_referrals = db.query(Referral).filter(
        Referral.referrer_id == user_id,
        Referral.is_completed == True
    ).count()

    return {
        "total_referrals": user.referral_count,
        "completed_referrals": completed_referrals,
        "total_earnings": user.referral_earnings
    }




@router.post("/complete")
def complete_referral(
    referrer_id: int,
    referred_user_id: int,
    reward_amount: int = 50,
    db: Session = Depends(get_db)
):
    referral = Referral(
        referrer_id=referrer_id,
        referred_user_id=referred_user_id,
        reward_amount=reward_amount,
        is_completed=True
    )

    referrer = db.query(User).filter(User.id == referrer_id).first()

    if not referrer:
        raise HTTPException(status_code=404, detail="Referrer not found")

    referrer.referral_count += 1
    referrer.referral_earnings += reward_amount

    db.add(referral)
    db.commit()

    return {
        "message": "Referral reward credited",
        "reward": reward_amount
    }