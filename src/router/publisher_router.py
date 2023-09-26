from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.user import User

from src.schema.publisher_schema import PublisherCreate, \
    PublisherModel, PublisherPut
from src.service import publisher_service
from src.service.user_service import get_current_user


router = APIRouter(
    prefix="/publisher",
    tags=["publisher"]
)


@router.post("/", response_model=PublisherModel)
def create_publisher(
    publisher: PublisherCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    return publisher_service.create_publisher(db, publisher)


@router.put("/", response_model=PublisherModel)
def put_publisher(
    publisher: PublisherPut,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    return publisher_service.put_publisher(db, publisher)


@router.get("/{publisher_id}", response_model=PublisherModel)
def get_publisher(
    publisher_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    return publisher_service.get_publisher(db, publisher_id)


@router.delete("/{publisher_id}")
def delete_publisher(
    publisher_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    publisher_service.delete_publisher(db, publisher_id)
    return {"message": "success"}
