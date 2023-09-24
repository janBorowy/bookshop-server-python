from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from src.database import get_db
from src.model.user import User
from src.security.login_security import hash
from test.test_integration.testing_data import test_data


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


def get_db_override():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_db_override
test_user = User(email="test@mail.com", hashed_password=hash("123"))


def get_test_user():
    return test_user


def populate_with_testing_data():
    db = TestingSessionLocal()
    db.add(test_user)
    for obj in test_data:
        print(f"saving object {obj}")
        db.add(obj)
    db.commit()
