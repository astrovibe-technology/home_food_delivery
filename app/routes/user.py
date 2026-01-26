from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.db import SessionLocal
from models.user import User
from database.login import MessageResponse,UserRegisterSchema
from lib_tu.utils import verify_password, create_access_token, get_password_hash



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

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        name=payload.name,
        email=email,
        password=get_password_hash(payload.password),
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"user_id": user.id})

    return {
        "message": "Login successful",
        # "access_token": token,
        # "token_type": "bearer"
    }


@router.post("/logout", response_model=MessageResponse)
def logout():
    # JWT stateless → frontend token delete
    return {"message": "Logout successful"}