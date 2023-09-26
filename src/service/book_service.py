import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query
from src.model.bookshop_model import Book

from src.schema.book_schema import BookCreate
from src.service import author_service, publisher_service
from sqlalchemy.exc import IntegrityError


def get_book(db: Session, book_isbn: str) -> Book:
    found_book = db.query(Book).filter(Book.isbn == book_isbn).first()
    if found_book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="no book with given isbn found")
    return found_book


def get_book_ignore_not_found(db: Session, book_isbn: str) -> Book | None:
    return db.query(Book).filter(Book.isbn == book_isbn).first()


def create_book(db: Session, book: BookCreate) -> Book:

    authors = author_service.fetch_authors(db, book.author_ids)
    publisher = publisher_service. \
        get_publisher_ignore_not_found(db, book.publisher_id)

    db_book = Book(
        isbn=book.isbn,
        title=book.title,
        published_date=book.published_date,
        cover_type=book.cover_type,
        number_of_pages=book.number_of_pages,
        dimensions=book.dimensions,
        price_in_us_cents=book.price_in_us_cents,
        publisher_price_in_us_cents=book.publisher_price_in_us_cents,
        cover_url=book.cover_url,
        publisher=publisher
    )

    db_book.authors = authors
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        logging.warning(e)
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Invalid book input")


def get_book_authors(db: Session, book_isbn: str):
    return get_book(book_isbn).authors


def delete_book(db: Session, book_isbn: str):
    found_book = get_book(db, book_isbn)
    db.delete(found_book)
    db.commit()


def replace_book(db: Session, book: BookCreate) -> Book:
    found_book = get_book_ignore_not_found(db, book_isbn=book.isbn)
    if found_book is not None:
        db.delete(found_book)
    return create_book(db, book)


def book_to_dict_representation(created_book: Book):
    return {
        **(created_book.__dict__),
        "authors": created_book.authors,
        "publisher": created_book.publisher
    }


def get_search_by_title_query(db: Session, prefix: str):
    return db.query(Book).filter(Book.title.like(f"{prefix}%"))


def paginate_query(query: Query, skip: int, limit: int) -> Query:
    return query.offset(skip).limit(limit)


def search_by_title(db: Session, prefix: str, skip: int, limit: int):
    query = get_search_by_title_query(db, prefix)

    return paginate_query(query, skip, limit).all()
