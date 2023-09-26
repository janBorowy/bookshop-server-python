from datetime import date
from pydantic import BaseModel, constr

from src.schema.author_schema import AuthorModel
from src.schema.publisher_schema import PublisherModel


isbn_regex = r"^\d{10}$|^\d{13}$"


class BookBase(BaseModel):
    title: constr(min_length=3, max_length=300)
    isbn: constr(pattern=isbn_regex)
    published_date: date
    cover_type: str
    number_of_pages: int | None = None
    dimensions: str | None = None
    price_in_us_cents: int | None = None
    publisher_price_in_us_cents: int
    cover_url: str | None = None


class BookCreate(BookBase):
    author_ids: list[int]
    publisher_id: int | None = None


class BookModel(BookBase):
    authors: list[AuthorModel]
    publisher: PublisherModel | None = None
