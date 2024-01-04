from typing import Optional

from pydantic import BaseModel


class AddDeliveryAddressRequestType(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    state: str
    city: str
    pin: str
    country: str
    landmark: str
    address_type: str
    is_default: bool
    delivery_to_phone: str
    delivery_to_person_name: str
