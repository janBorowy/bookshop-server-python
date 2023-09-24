from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import constr

from sqlalchemy.orm import Session
from src.database import get_db
from src.exception.service_exceptions import NotAllAuthorsExist
from src.model.user import User
from src.schema.book_schema import BookCreate, BookModel, isbn_regex
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
    return {
        **(created_book.__dict__),
        "authors": created_book.authors
    }


@router.get("/{book_isbn}", response_model=BookModel)
def get_book(book_isbn: str,
             db: Annotated[Session, Depends(get_db)],
             user: Annotated[User, Depends(get_current_user)]):
    return book_service.get_book(db, book_isbn)


@router.patch("/", response_model=BookModel)
def patch_book():
    return {}


@router.delete("/{book_isbn}")
def delete_book():
    return {"message": "success"}
