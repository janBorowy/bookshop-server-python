from ..database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "bookshop_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
