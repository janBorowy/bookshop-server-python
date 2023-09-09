from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserModel(UserBase):
    id: int

    class Config:
        from_attributes = True
