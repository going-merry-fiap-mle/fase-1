import uuid
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.domain.models.book_domain_model import Book as DomainBook
from app.domain.models.category_domain_model import Category as DomainCategory
from app.infrastructure.models.book import Book as ORMBook
from app.infrastructure.models.category import Category as ORMCategory
from app.infrastructure.repository.book_repository import BookRepository
from app.infrastructure.repository.scraping_repository import ScrapingRepository
from app.schemas.scraping_schema import ScrapingBase


def make_scraping_base(
    title="T",
    price="£10.00",
    rating=4,
    availability="In stock",
    category="F",
    image="img",
):
    return ScrapingBase(
        title=title,
        price=price,
        rating=rating,
        availability=availability,
        category=category,
        image_url=image,
    )


def test_convert_to_domain_books_creates_domain_models():
    with patch("app.infrastructure.repository.scraping_repository.get_session"):
        pass


def test_book_repository_to_domain_conversion():
    book_id = uuid.uuid4()
    category_id = uuid.uuid4()

    orm_category = ORMCategory(name="Cat")
    orm_category.id = category_id

    orm_book = ORMBook(
        title="Title",
        price=Decimal("12.34"),
        availability="In stock",
        category_id=category_id,
        image_url="img.jpg",
        rating=5,
    )
    orm_book.id = book_id
    orm_book.category = orm_category

    repo = BookRepository()

    with patch(
        "app.infrastructure.repository.book_repository.get_session"
    ) as get_session:
        session = MagicMock()
        session.query.return_value.count.return_value = 1
        session.query.return_value.offset.return_value.limit.return_value.all.return_value = [orm_book]
        get_session.return_value.__enter__.return_value = session

        books, total = repo.get_books()

        assert len(books) == 1
        assert total == 1
        b = books[0]
        assert isinstance(b, DomainBook)
        assert b.title == "Title"
        assert b.category.name == "Cat"


def test_scraping_repository_bulk_insert_creates_categories_and_inserts_books():
    cat = DomainCategory(name="Fiction")
    domain_book = DomainBook(
        id=uuid.uuid4(),
        title="B",
        price=Decimal("9.99"),
        rating=4,
        availability="In stock",
        category=cat,
        image_url="img",
    )

    repo = ScrapingRepository()

    with patch(
        "app.infrastructure.repository.scraping_repository.get_session"
    ) as get_session, patch.object(
        repo, "_category_repository", autospec=True
    ) as mock_cat_repo:

        session = MagicMock()
        get_session.return_value.__enter__.return_value = session

        returned_cat = DomainCategory(name="Fiction", id=uuid.uuid4())
        mock_cat_repo.get_or_create_by_name.return_value = returned_cat

        with patch("app.infrastructure.models.book.Book.from_domain") as from_domain:
            mock_orm_book = ORMBook(
                title="Mock",
                price=Decimal("1.00"),
                availability="In stock",
                category_id=uuid.uuid4(),
                image_url="mock.jpg",
            )
            from_domain.return_value = mock_orm_book

            repo.scraping_bulk_insert([domain_book])

            mock_cat_repo.get_or_create_by_name.assert_called_once_with("Fiction")

            session.bulk_save_objects.assert_called_once()
            session.flush.assert_called_once()
