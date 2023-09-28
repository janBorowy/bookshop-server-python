from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.exception.service_exceptions import NotAllAuthorsExist

from src.model.bookshop_model import Author
from src.schema.author_schema import AuthorBase, AuthorCreate, AuthorPatch


def get_author(db: Session, author_id: int) -> Author:
    found_author = db.query(Author).filter(Author.id == author_id).first()
    if found_author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="author not found")
    return found_author


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(
        name=author.name,
        lastname=author.lastname,
        books=[],
        portrait_url=get_author_portrait_url_string_if_exists(author)
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    author = get_author(db, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="author not found")
    db.delete(author)
    db.commit()


def fetch_authors(db: Session, author_ids: list[int]):
    authors = []
    for id in author_ids:
        found_author = get_author(db, id)
        if found_author is None:
            raise NotAllAuthorsExist("not all given authors exist")
        authors.append(found_author)
    return authors


def update_author(db: Session, author: AuthorPatch):
    author_id = author.id
    db_author = get_author(db, author_id)

    if db_author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="author not found")

    if author.name is not None:
        db_author.name = author.name
    if author.lastname is not None:
        db_author.lastname = author.lastname
    if author.portrait_url is not None:
        db_author.portrait_url = \
            get_author_portrait_url_string_if_exists(author)

    db.commit()
    return db_author


def get_author_portrait_url_string_if_exists(
        author: AuthorBase) -> str | None:
    if author.portrait_url is not None:
        return str(author.portrait_url)
    return None
