from starlette.testclient import TestClient


class TestPublisherGet:
    def test_successful(self, client: TestClient):
        result = client.get("/publisher/1")

        assert result.status_code == 200
        assert result.json() == {
            "name": "SuperNowa",
            "id": 1
        }

    def test_not_found(self, client: TestClient):
        result = client.get("/publisher/100")

        assert result.status_code == 404


class TestPublisherPost:
    def test_successful(self, client: TestClient):
        body = {
            "name": "Grupa Wydawnicza Helion"
        }

        result = client.post("/publisher/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body["id"] == 2
        assert result_body["name"] == "Grupa Wydawnicza Helion"


class TestPublisherPut:
    def test_successful_replace(self, client: TestClient):
        body = {
            "id": 2,
            "name": "Grupa Wydawnicza Klepion"
        }

        result = client.put("/publisher/", json=body)

        assert result.status_code == 200
        assert result.json() == {
            "id": 2,
            "name": "Grupa Wydawnicza Klepion"
        }

    def test_successful_create(self, client: TestClient):
        body = {
            "id": 100,
            "name": "Tor Books"
        }

        result = client.put("/publisher/", json=body)

        assert result.status_code == 200
        assert result.json() == {
            "id": 100,
            "name": "Tor Books"
        }


class TestPublisherDelete:
    def test_successful(self, client: TestClient):

        result_1 = client.delete("/publisher/2")
        result_2 = client.delete("/publisher/100")

        assert result_1.status_code == 200
        assert result_2.status_code == 200

    def test_not_found(self, client: TestClient):

        result = client.delete("/publisher/2")

        assert result.status_code == 404
