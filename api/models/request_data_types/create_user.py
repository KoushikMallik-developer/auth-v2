# from typing import Optional

from pydantic import BaseModel


class CreateUserRequestType(BaseModel):
    fname: str
    lname: str
    username: str
    email: str
    password1: str
    password2: str
