from starlette.testclient import TestClient


class TestAuthorCreate:

    def test_valid_request(self, client: TestClient):
        body = {
            "name": "Andrzej",
            "lastname": "Sapkowski",
            "id": 10
        }

        result = client.post("/author/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["id"] == 1
        assert result_body["name"] == "Andrzej"
        assert result_body["lastname"] == "Sapkowski"

    def test_invalid_name(self, client: TestClient):
        body = {
            "name": "A",
            "lastname": "Sapkowski",
            "id": 10
        }

        result = client.post("/author/", json=body)

        assert result.status_code == 422

    def test_invalid_lastname(self, client: TestClient):
        body = {
            "name": "Andrzej",
            "lastname": "S",
            "id": 10
        }

        result = client.post("/author/", json=body)

        assert result.status_code == 422


class TestAuthorPatch:

    def test_valid_input(self, client: TestClient):
        body = {
            "name": "Janusz",
            "id": 1
        }

        result = client.patch("/author/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["name"] == "Janusz"
        assert result_body["lastname"] == "Sapkowski"
        assert result_body["id"] == 1

    def test_invalid_attribute(self, client: TestClient):
        body = {
            "name": "J",
            "id": 1
        }

        result = client.patch("/author/", json=body)

        assert result.status_code == 422

    def test_author_not_found(self, client: TestClient):
        body = {
            "id": 2
        }

        result = client.patch("/author/", json=body)

        assert result.status_code == 404


class TestAuthorGet:

    def test_successful(self, client: TestClient):
        result = client.get("/author/1")
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["name"] == "Janusz"
        assert result_body["lastname"] == "Sapkowski"

    def test_not_found(self, client: TestClient):
        result = client.get("/author/2")

        assert result.status_code == 404


class TestAuthorDelete:

    def test_successful(self, client: TestClient):

        result = client.delete("/author/1")

        assert result.status_code == 200

    def test_not_found(self, client: TestClient):

        result = client.delete("/author/1")

        assert result.status_code == 404
