from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..schema.token_schema import Token, TokenData
from ..schema.user_schema import UserLogin
from ..service import user_service
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Annotated
from ..exception.http_exceptions import credentials_exception
from datetime import datetime
import secrets


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash(to_hash: str):
    return pwd_context.hash(to_hash)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expiration_time: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expiration_time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


token_router = APIRouter(
    prefix="",
    tags=["token"]
)


@token_router.post("/token", response_model=Token)
def get_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user_login = UserLogin(email=form.username, password=form.password)
    user = user_service.authenticate_user(db, user_login)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expiration_time=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}


def get_logged_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
