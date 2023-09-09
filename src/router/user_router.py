from fastapi import APIRouter, HTTPException, status, Body
from ..schema.user_schema import UserCreate, UserModel
from typing import Annotated
from ..database import get_db
from ..service import user_service
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/",response_model=UserModel)
def create_user(user: Annotated[UserCreate, Body()], db: Annotated[Session, Depends(get_db)]):
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    return user_service.create_user(user)