from sqlalchemy.orm import Session
from ..model.user import User
from ..security.login_security import hash, verify_password, oauth2_scheme, get_logged_user
from ..schema.user_schema import UserCreate, UserLogin
from fastapi import HTTPException, status, Depends
from typing import Annotated


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user_login: UserLogin) -> User:
    user = get_user_by_email(db, user_login.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    return user


def get_current_user(user: Annotated[User, Depends(get_logged_user)]):
    return user