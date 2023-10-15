import datetime
import typing
from typing import Optional

from pydantic import BaseModel


class ExportECOMUser(BaseModel):
    id: str
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
            kwargs["image"] = kwargs.get("image").url
        if not kwargs.get("id"):
            kwargs["id"] = kwargs.get("email")
        super().__init__(**kwargs)


class ExportECOMUserList(BaseModel):
    user_list: typing.List[ExportECOMUser]
