from starlette.testclient import TestClient


class TestBookGet:

    def test_successful(self, client: TestClient):
        result = client.get("/book/9788375780635")
        result_body = result.json()

        assert result_body == {
            "isbn": "9788375780635",
            "title": "Wiedźmin: Ostatnie życzenie",
            "authors": [
                {
                    "name": "Andrzej",
                    "lastname": "Sapkowski",
                    "id": 1
                },
            ],
            "published_date": "2014-01-01",
            "publisher": {
                "name": "SuperNowa",
                "id": 1
            },
            "cover_type": "paperback",
            "number_of_pages": 332,
            "dimensions": "4.96x1.06x7.68in",
            "price_in_us_cents": 999,
            "publisher_price_in_us_cents": 1499,
            "cover_url": "https://m.media-amazon.com/images/I/71lNI3qT32L._SY466_.jpg"
        }

    def test_not_found(self, client: TestClient):

        result = client.get("/book/1234567890")

        assert result.status_code == 404


class TestBookPost:

    def test_successful(self, client: TestClient):
        author_create_body = {
            "name": "Robert",
            "lastname": "Jordan"
        }

        author_result = client.post("/author/", json=author_create_body)
        author_result_body = author_result.json()

        body = {
            "title": "The Wheel of Time",
            "isbn": "0812540115",
            "author_ids": [
                author_result_body["id"]
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999
        }

        result = client.post("/book/", json=body)
        result_body = result.json()

        assert result.status_code == 200
        assert result_body == {
            "title": "The Wheel of Time",
            "isbn": "0812540115",
            "authors": [{
                **author_create_body,
                "id": author_result_body["id"]
            }],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999,
            "number_of_pages": None,
            "dimensions": None,
            "price_in_us_cents": None,
            "cover_url": None,
            "publisher": None,
        }

    def test_no_isbn(self, client: TestClient):
        author_create_body = {
            "name": "Robert",
            "lastname": "Jordan"
        }

        author_result = client.post("/author/", json=author_create_body)
        author_result_body = author_result.json()

        body = {
            "title": "The Wheel of Time",
            "author_ids": [
                author_result_body["id"]
            ]
        }

        result = client.post("/book/", json=body)

        result.status_code == 422

    def test_author_does_not_exist(self, client: TestClient):
        body = {
            "title": "The Wheel of Time",
            "isbn": "0812540115",
            "author_ids": [
                5
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999
        }

        result = client.post("/book/", json=body)

        assert result.status_code == 404

    def test_already_exists(self, client: TestClient):
        body = {
            "isbn": "9788375780635",
            "title": "Wiedźmin: Ostatnie psioczenie",
            "author_ids": [
                1
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999
        }

        result = client.post("/book/", json=body)

        assert result.status_code == 403


class TestBookPut:

    def test_successful(self, client: TestClient):
        body = {
            "title": "The Wheel of Fire",
            "isbn": "0812540115",
            "author_ids": [
                1
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999
        }

        result = client.put("/book/", json=body)

        assert result.status_code == 200
        assert result.json() == {
            "title": "The Wheel of Fire",
            "isbn": "0812540115",
            "authors": [
                {
                    "name": "Andrzej",
                    "lastname": "Sapkowski",
                    "id": 1
                }
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999,
            "number_of_pages": None,
            "dimensions": None,
            "price_in_us_cents": None,
            "cover_url": None,
            "publisher": None,
        }

    def test_new_book(self, client: TestClient):
        body = {
            "title": "The Wheel of Fire",
            "isbn": "1234567890",
            "author_ids": [
                1
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999
        }

        result = client.put("/book/", json=body)

        assert result.status_code == 200
        assert result.json() == {
            "title": "The Wheel of Fire",
            "isbn": "1234567890",
            "authors": [
                {
                    "name": "Andrzej",
                    "lastname": "Sapkowski",
                    "id": 1
                }
            ],
            "published_date": "1990-01-15",
            "cover_type": "paperback",
            "publisher_price_in_us_cents": 999,
            "number_of_pages": None,
            "dimensions": None,
            "price_in_us_cents": None,
            "cover_url": None,
            "publisher": None,
        }


class TestBookDelete:

    def test_successful(self, client: TestClient):
        result = client.delete("/book/0812540115")

        assert result.status_code == 200

    def test_book_does_not_exist(self, client: TestClient):
        result = client.delete("/book/0812540115")

        assert result.status_code == 404


class TestSearchByTitle:
    def test_find_one(self, client: TestClient):

        result = client.get("/book/search-by-title?phrase=Wie")

        assert result.status_code == 200
        assert result.json() == [
            {
                "isbn": "9788375780635",
                "title": "Wiedźmin: Ostatnie życzenie",
                "authors": [
                    {
                        "name": "Andrzej",
                        "lastname": "Sapkowski",
                        "id": 1
                    },
                ],
                "published_date": "2014-01-01",
                "publisher": {
                    "name": "SuperNowa",
                    "id": 1
                },
                "cover_type": "paperback",
                "number_of_pages": 332,
                "dimensions": "4.96x1.06x7.68in",
                "price_in_us_cents": 999,
                "publisher_price_in_us_cents": 1499,
                "cover_url": "https://m.media-amazon.com/images/I/71lNI3qT32L._SY466_.jpg"
            }
        ]

    def test_find_none(self, client: TestClient):
        result = client.get("/book/search-by-title?phrase=nonexis")

        assert result.json() == []
