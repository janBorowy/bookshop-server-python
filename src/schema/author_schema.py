from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    lastname: str


class AuthorCreate(AuthorBase):
    pass


class AuthorModel(AuthorBase):
    id: int
