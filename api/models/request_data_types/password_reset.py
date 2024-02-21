from pydantic import BaseModel


class PasswordResetRequestType(BaseModel):
    email: str
