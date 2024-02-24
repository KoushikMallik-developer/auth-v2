from pydantic import BaseModel


class UpdatePasswordRequestType(BaseModel):
    user_id: str
