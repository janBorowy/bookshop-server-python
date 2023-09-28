from starlette.testclient import TestClient


class TestAuthorCreate:

    def test_valid_request(self, client: TestClient):
        body = {
            "name": "Andrzej",
            "lastname": "Sapkowski",
            "portrait_url": "https://i.imgur.com/piEoGdM.jpeg",
            "id": 10
        }

        result = client.post("/author/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["id"] == 3
        assert result_body["name"] == "Andrzej"
        assert result_body["lastname"] == "Sapkowski"

    def test_invalid_name(self, client: TestClient):
        body = {
            "name": "A",
            "lastname": "Sapkowski",
            "portrait_url": "https://i.imgur.com/piEoGdM.jpeg",
            "id": 10
        }

        result = client.post("/author/", json=body)

        assert result.status_code == 422

    def test_invalid_url(self, client: TestClient):
        body = {
            "name": "Andrzej",
            "lastname": "S",
            "portrait_url": "xd://www.funnyimage.pl",
            "id": 10
        }

        result = client.post("/author/", json=body)

        assert result.status_code == 422


class TestAuthorPatch:

    def test_valid_input(self, client: TestClient):
        body = {
            "name": "Janusz",
            "id": 3
        }

        result = client.patch("/author/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["name"] == "Janusz"
        assert result_body["lastname"] == "Sapkowski"
        assert result_body["id"] == 3

    def test_invalid_attribute(self, client: TestClient):
        body = {
            "name": "J",
            "id": 3
        }

        result = client.patch("/author/", json=body)

        assert result.status_code == 422

    def test_author_not_found(self, client: TestClient):
        body = {
            "id": 4
        }

        result = client.patch("/author/", json=body)

        assert result.status_code == 404


class TestAuthorGet:

    def test_successful(self, client: TestClient):
        result = client.get("/author/3")
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["name"] == "Janusz"
        assert result_body["lastname"] == "Sapkowski"
        assert result_body["portrait_url"] == "https://i.imgur.com/piEoGdM.jpeg"

    def test_not_found(self, client: TestClient):
        result = client.get("/author/4")

        assert result.status_code == 404


class TestAuthorDelete:

    def test_successful(self, client: TestClient):

        result = client.delete("/author/3")

        assert result.status_code == 200

    def test_not_found(self, client: TestClient):

        result = client.delete("/author/3")

        assert result.status_code == 404
