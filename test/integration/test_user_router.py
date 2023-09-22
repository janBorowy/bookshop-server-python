from starlette.testclient import TestClient


def test_create_user(client: TestClient):
    body = {
        "email": "testmail@mail.com",
        "password": "123"
    }

    result = client.post("/user/", body=body)

    
