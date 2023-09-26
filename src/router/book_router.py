from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from src.database import get_db
from src.exception.service_exceptions import NotAllAuthorsExist
from src.model.bookshop_model import Book
from src.model.user import User
from src.schema.book_schema import BookCreate, BookModel
from src.service import book_service
from src.service.user_service import get_current_user


router = APIRouter(
    prefix="/book",
    tags=["book"]
)


@router.post("/", response_model=BookModel)
def create_book(
    book: BookCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        created_book = book_service.create_book(db, book)
    except NotAllAuthorsExist as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e)
    return book_service.book_to_dict_representation(created_book)


@router.get("/search-by-title", response_model=list[BookModel])
def search_for_book_by_title(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    phrase: str = "",
    skip: int = 0,
    limit: int = 10
):
    return book_service.search_by_title(db, phrase, skip, limit)


@router.get("/{book_isbn}", response_model=BookModel)
def get_book(book_isbn: str,
             db: Annotated[Session, Depends(get_db)],
             user: Annotated[User, Depends(get_current_user)]):
    return book_service.get_book(db, book_isbn)


@router.put("/", response_model=BookModel)
def put_book(
    book: BookCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]):
    created_book = book_service.replace_book(db, book)
    return book_service.book_to_dict_representation(created_book)


@router.delete("/{book_isbn}")
def delete_book(book_isbn: str,
                db: Annotated[Session, Depends(get_db)],
                user: Annotated[User, Depends(get_current_user)]):
    book_service.delete_book(db, book_isbn)
    return {"message": "success"}
