from typing import Optional

from pydantic import BaseModel


class ExportAddress(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    state: str
    city: str
    pin: str
    country: str
    landmark: str
