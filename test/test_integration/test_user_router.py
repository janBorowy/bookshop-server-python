from starlette.testclient import TestClient


class TestCreateUser:

    def test_valid_request(self, client: TestClient):
        body = {
            "email": "testmail@mail.com",
            "password": "123"
        }

        result = client.post("/user/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["email"] == "testmail <testmail@mail.com>"
        assert result_body["id"] is not None

    def test_invalid_email(self, client: TestClient):
        body = {
            "email": "testuser",
            "password": "123"
        }

        result = client.post("/user/", json=body)

        assert result.status_code == 422
