import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ExportDeliveryAddress(BaseModel):
    id: UUID
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
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ExportDeliveryAddressList(BaseModel):
    address_list: typing.List[ExportDeliveryAddress]
