

from src.model.bookshop_model import Author, Book


example_author_1 = Author(name="Andrzej", lastname="Sapkowski")
example_author_2 = Author(name="Ernest", lastname="Hemingway")

example_book_1 = Book(isbn="9788375780635",
                      title="Wiedźmin: Ostatnie życzenie",
                      authors=[example_author_1])


test_data = [
    example_author_1,
    example_author_2,
    example_book_1
]
