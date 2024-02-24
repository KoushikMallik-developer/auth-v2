from pydantic import BaseModel


class RemoveUserRequestType(BaseModel):
    email: str
