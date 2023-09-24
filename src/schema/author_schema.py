from pydantic import BaseModel, constr


class AuthorBase(BaseModel):
    name: constr(min_length=3)
    lastname: constr(min_length=3)


class AuthorPatch(BaseModel):
    id: int
    name: constr(min_length=3) | None = None
    lastname: constr(min_length=3) | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorModel(AuthorBase):
    id: int
