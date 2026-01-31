from pydantic import BaseModel

class ShopCreate(BaseModel):
    shop_name: str
    address: str
    certificate_no: str | None = None
    gst_number: str | None = None
    bank_name: str | None = None
    account_number: str | None = None
    IFSC_Code: str | None = None


class ShopUpdate(BaseModel):
    shop_name: str | None = None
    address: str | None = None
    certificate_no: str | None = None
    gst_number: str | None = None
    bank_name: str | None = None
    account_number: str | None = None
    IFSC_Code: str | None = None