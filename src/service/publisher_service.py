from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.model.bookshop_model import Publisher

from src.schema.publisher_schema import PublisherCreate, PublisherPut


def get_publisher_ignore_not_found(db: Session,
                                   publisher_id: int) -> Publisher | None:
    return db.query(Publisher).filter(Publisher.id == publisher_id).first()


def get_publisher(db: Session, publisher_id: int) -> Publisher:
    found_publisher = get_publisher_ignore_not_found(db, publisher_id)
    if found_publisher is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="publisher not found")
    return found_publisher


def create_publisher(db: Session,
                     publisher: PublisherCreate,
                     id: int = None) -> Publisher:
    publisher_db = Publisher(
        name=publisher.name,
        id=id
    )

    db.add(publisher_db)
    db.commit()
    db.refresh(publisher_db)
    return publisher_db


def delete_publisher(db: Session, publisher_id: str):
    found_publisher = get_publisher(db, publisher_id)
    db.delete(found_publisher)
    db.commit()


def put_publisher(db: Session, publisher: PublisherPut) -> Publisher:
    found_publisher = get_publisher_ignore_not_found(db, publisher.id)
    if found_publisher is not None:
        db.delete(found_publisher)
    return create_publisher(db, publisher, id=publisher.id)
