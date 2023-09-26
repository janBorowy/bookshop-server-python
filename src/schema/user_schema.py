from pydantic import BaseModel, NameEmail


class UserBase(BaseModel):
    email: NameEmail


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    password: str


class UserModel(UserBase):
    id: int

    class Config:
        from_attributes = True
