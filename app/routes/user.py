from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import Request
import random
from datetime import datetime, timedelta

from database.db import SessionLocal
from models.user import User
from database.login import MessageResponse, UserRegisterSchema, LoginSchema
from lib_tu.mail import send_mail
from lib_tu.utils import verify_password, create_access_token, get_password_hash, generate_referral_code

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(
    payload: UserRegisterSchema,
    role: str = "user",   
    db: Session = Depends(get_db)
):
    email = payload.email.lower()
    phone = payload.phone_number.strip()

    existing = db.query(User).filter(
        or_(
            User.email == email,
            User.phone == phone
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    referral_code = generate_referral_code()

    user = User(
        name=payload.name,
        email=email,
        phone=phone,
        password=get_password_hash(payload.password),
        is_active=True,
        role=role.lower(),       
        referral_code=referral_code
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": f"{user.role} registered successfully",
        "referral_code": user.referral_code,
        "role": user.role
    }


@router.post("/login")
def login(
    payload: LoginSchema,
    db: Session = Depends(get_db)
):
    identifier = payload.email_or_phone.strip()


    if "@" in identifier:
        user = db.query(User).filter(
            User.email == identifier.lower()
        ).first()
    else:
        user = db.query(User).filter(
            User.phone == identifier
        ).first()


    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email or phone number not found"
        )


    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )


    token = create_access_token({"user_id": user.id})

    return {
        "message": "Login successful",
        "access_token": token,
        # "token_type": "bearer"
    }

@router.post("/logout", response_model=MessageResponse)
def logout():
    return {"message": "Logout successful"}



FAKE_DOMAINS = ["test.com", "example.com", "mailinator.com"]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_fake_email(email: str) -> bool:
    """Check if email is fake by domain"""
    domain = email.split("@")[-1].lower()
    return domain in FAKE_DOMAINS

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    if user.is_fake_mail or is_fake_email(email):
        
        raise HTTPException(status_code=404, detail="User not found")

   
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    
    user.reset_otp = otp
    user.otp_expiry = expiry
    db.commit()

   
    send_mail(
        to_email=user.email,
        subject="Password Reset OTP",
        body=f"Your OTP is {otp}. Valid for 5 minutes."
    )

    return {
        "message": "OTP sent to registered email"
    }

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.reset_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    
    user.is_otp_verified = True
    db.commit()

    return {"message": "OTP verified successfully"}



@router.post("/reset-password")
def reset_password(
    new_password: str,
    confirm_password: str,
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter(User.is_otp_verified == True).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="OTP verification required"
        )

    
    if new_password != confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match"
        )

    
    user.password = get_password_hash(new_password)

    
    user.reset_otp = None
    user.otp_expiry = None
    user.is_otp_verified = False

    db.commit()

    return {"message": "Password reset successfully"}