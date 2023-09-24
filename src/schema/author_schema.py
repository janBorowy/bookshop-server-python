from pydantic import BaseModel, constr


class AuthorBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    lastname: constr(min_length=3, max_length=100)


class AuthorPatch(BaseModel):
    id: int
    name: constr(min_length=3, max_length=100) | None = None
    lastname: constr(min_length=3, max_length=100) | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorModel(AuthorBase):
    id: int
