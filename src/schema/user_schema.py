from pydantic import BaseModel, NameEmail


class UserBase(BaseModel):
    email: NameEmail


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserModel(UserBase):
    id: int

    class Config:
        from_attributes = True
