from pydantic import BaseModel, constr

from src.schema.author_schema import AuthorModel


isbn_regex = r"^\d{10}$|^\d{13}$"


class BookBase(BaseModel):
    title: constr(min_length=3, max_length=300)
    isbn: constr(pattern=isbn_regex)


class BookCreate(BookBase):
    author_ids: list[int]


class BookModel(BookBase):
    authors: list[AuthorModel]
