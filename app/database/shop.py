from pydantic import BaseModel
from typing import Optional

class ShopCreate(BaseModel):
    shop_name: str
    address: str
    certificate_no: str | None = None
    gst_number: str | None = None
    bank_name: str | None = None
    account_number: str | None = None
    IFSC_Code: str | None = None


class ShopUpdate(BaseModel):
    shop_name: Optional[str] = None
    address: Optional[str] = None
    certificate_no: Optional[str] = None
    gst_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    IFSC_Code: Optional[str] = None

    class Config:
        from_attributes = True