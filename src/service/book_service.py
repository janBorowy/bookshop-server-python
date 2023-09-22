from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from src.model.bookshop_model import Author, Book

from src.schema.book_schema import BookCreate
from src.service import author_service


def get_book(db: Session, book_isbn: int):
    found_book = db.query(Book).filter(Book.isbn == book_isbn).first()
    if found_book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="no book with given isbn")
    return found_book


def create_book(db: Session, book: BookCreate) -> Book:
    
    authors = author_service.fetch_authors(db, book.author_ids)
    
    db_book = Book(
        isbn=book.isbn,
        title=book.title
    )

    db_book.authors = authors

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_authors(db: Session, book_isbn: str):
    return get_book(book_isbn).authors