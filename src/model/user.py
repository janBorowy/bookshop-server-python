from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "bookshop_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
