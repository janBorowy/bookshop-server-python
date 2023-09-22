from pydantic import BaseModel

from src.schema.author_schema import AuthorModel


class BookBase(BaseModel):
    title: str
    isbn: str

class BookCreate(BookBase):
    author_ids: list[int]

class BookModel(BookBase):
    authors: list[AuthorModel]