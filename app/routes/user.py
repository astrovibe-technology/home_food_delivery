from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.db import SessionLocal
from models.user import User
from database.login import MessageResponse, UserRegisterSchema, LoginSchema
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
        referral_code=referral_code  
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "referral_code": user.referral_code
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
        # "access_token": token,
        # "token_type": "bearer"
    }

@router.post("/logout", response_model=MessageResponse)
def logout():
    return {"message": "Logout successful"}