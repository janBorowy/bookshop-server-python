from fastapi.testclient import TestClient
from pytest import fixture
from src.database import Base
from main import app
from src.security.login_security import get_logged_user
from test.test_integration.database_testing import get_db_override, \
    engine, get_test_user, populate_with_testing_data


@fixture(scope="session")
def client() -> TestClient:
    return TestClient(app=app)


@fixture()
def get_database_connection():
    return get_db_override()


@fixture(scope="session", autouse=True)
def reload_database_state():
    Base.metadata.create_all(bind=engine)
    populate_with_testing_data()
    yield
    Base.metadata.drop_all(bind=engine)


@fixture(scope="session", autouse=True)
def login_test_user():
    app.dependency_overrides[get_logged_user] = get_test_user
