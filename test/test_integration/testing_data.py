from datetime import date
from src.model.bookshop_model import Author, Book, Publisher


example_author_1 = Author(name="Andrzej",
                          lastname="Sapkowski",
                          portrait_url="https://api.culture.pl/sites/default/files/styles/1920_auto/public/2018-06/andrzejsapkowski_en.jpg?itok=ZEZz-hGr"
                          )
example_author_2 = Author(name="Ernest", lastname="Hemingway")
example_publisher_1 = Publisher(name="SuperNowa")

example_book_1 = Book(isbn="9788375780635",
                      title="Wiedźmin: Ostatnie życzenie",
                      authors=[example_author_1],
                      published_date=date(2014, 1, 1),
                      publisher=example_publisher_1,
                      cover_type="paperback",
                      number_of_pages=332,
                      dimensions="4.96x1.06x7.68in",
                      price_in_us_cents=999,
                      publisher_price_in_us_cents=1499,
                      cover_url="https://m.media-amazon.com/images/I/71lNI3qT32L._SY466_.jpg"
                      )


test_data = [
    example_author_1,
    example_author_2,
    example_publisher_1,
    example_book_1
]
