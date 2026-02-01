from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    email_or_phone: str
    password: str

class MessageResponse(BaseModel):
    message: str

class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    referral_code: str