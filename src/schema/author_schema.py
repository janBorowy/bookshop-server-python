from pydantic import BaseModel, HttpUrl, constr


class AuthorBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    lastname: constr(min_length=3, max_length=100)
    portrait_url: HttpUrl | None = None


class AuthorPatch(BaseModel):
    id: int
    name: constr(min_length=3, max_length=100) | None = None
    lastname: constr(min_length=3, max_length=100) | None = None
    portrait_url: HttpUrl | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorModel(AuthorBase):
    id: int
