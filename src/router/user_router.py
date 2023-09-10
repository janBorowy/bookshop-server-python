from fastapi import APIRouter, HTTPException, status, Depends
from ..model.user import User
from ..schema.user_schema import UserCreate, UserModel
from typing import Annotated
from ..database import get_db
from ..service import user_service
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=UserModel)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    return user_service.create_user(db, user)


@router.post("/hello")
def say_hello(logged_user: Annotated[User, Depends(user_service.get_current_user)]):
    return { "message": f"Hello {logged_user.email}!"}