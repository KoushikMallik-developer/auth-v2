from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from api.models.response_data_types.response_data import ResponseData


class SignInResponseData(ResponseData):
    token: Optional[VerificationToken]


class VerificationToken(BaseModel):
    access: str
    refresh: str
