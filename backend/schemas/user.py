from pydantic import BaseModel
from pydantic import Field


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: int
    username: str
    is_active: bool

    class ConfigDict:
        from_attributes = True
