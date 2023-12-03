import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ExportECOMUser(BaseModel):
    id: UUID
    username: str
    email: str
    fname: str
    lname: str
    dob: Optional[datetime.datetime]
    phone: Optional[str]
    image: Optional[str]
    is_active: bool
    account_type: str

    def __init__(self, **kwargs):
        if kwargs.get("image"):
            if not isinstance(kwargs.get("image"), str):
                kwargs["image"] = kwargs.get("image").url
            else:
                kwargs["image"] = None
        super().__init__(**kwargs)


class ExportECOMUserList(BaseModel):
    user_list: typing.List[ExportECOMUser]
