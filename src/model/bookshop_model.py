from datetime import date
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


book_author_assiciation_table = Table(
    "book_author",
    Base.metadata,
    Column("book_isbn", ForeignKey("book.isbn")),
    Column("author_id", ForeignKey("author.id"))
)


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    lastname: Mapped[str] = mapped_column(index=True)
    books: Mapped[List["Book"]] = relationship(
        secondary=book_author_assiciation_table,
        back_populates="authors"
        )
    portrait_url: Mapped[Optional[str]]


class Publisher(Base):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    books: Mapped[List["Book"]] = relationship(back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    isbn: Mapped[str] = mapped_column(String(13), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    authors: Mapped[List["Author"]] = relationship(
        secondary=book_author_assiciation_table,
        back_populates="books"
        )
    published_date: Mapped[date]
    publisher_id: Mapped[Optional[int]] = \
        mapped_column(ForeignKey("publisher.id"))
    publisher: Mapped[Optional["Publisher"]] = \
        relationship(back_populates="books")
    cover_type: Mapped[str]
    number_of_pages: Mapped[Optional[int]]
    dimensions: Mapped[Optional[str]]
    price_in_us_cents: Mapped[Optional[int]]
    publisher_price_in_us_cents: Mapped[int]
    cover_url: Mapped[Optional[str]]
