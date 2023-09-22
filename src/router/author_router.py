from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.user import User

from src.schema.author_schema import AuthorModel, AuthorCreate
from src.service import author_service, user_service


router = APIRouter(
    prefix="/author",
    tags=["author"]
)

@router.post("/", response_model=AuthorModel)
def create_author(
    author: AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(user_service.get_current_user)]):
    created_author = author_service.create_author(db, author)
    return created_author

@router.delete("/{author_id}")
def delete_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(user_service.get_current_user)]):
    author_service.delete_author(db, author_id)
    return {"message": "success"}


@router.get("/{author_id}")
def get_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(user_service.get_current_user)]):
    return author_service.get_author(db, author_id)