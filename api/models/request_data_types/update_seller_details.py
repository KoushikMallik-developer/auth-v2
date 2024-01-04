from typing import Optional

from pydantic import BaseModel


class UpdateSellerDetailsRequestType(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    dob: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None
    company_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pin: Optional[str] = None
    country: Optional[str] = None
    landmark: Optional[str] = None
