from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    lastname: str


class AuthorPatch(BaseModel):
    id: int
    name: str | None = None
    lastname: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorModel(AuthorBase):
    id: int
