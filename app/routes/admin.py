from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy import or_



router = APIRouter(prefix="/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def admin_login(
    email_or_phone: str,
    password: str,
    db: Session = Depends(get_db)
):

    
    user = db.query(User).filter(
        or_(
            User.email == email_or_phone,
            User.phone == email_or_phone
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    if user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admin only")

    
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    
    access_token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

   
    return {
        "message": "Admin login successful",
        "role": user.role,
        "access_token": access_token
    }