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
    orm_book = ORMBook(
        id=uuid.uuid4(),
        title="Title",
        price=Decimal("12.34"),
        rating=5,
        availability="In stock",
        image_url="img.jpg",
    )

    orm_category = ORMCategory(id=uuid.uuid4(), name="Cat")
    orm_book.category = orm_category

    repo = BookRepository()

    with patch(
        "app.infrastructure.repository.book_repository.get_session"
    ) as get_session:
        session = MagicMock()
        session.query.return_value.all.return_value = [orm_book]
        get_session.return_value.__enter__.return_value = session

        books = repo.get_books()

        assert len(books) == 1
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
            from_domain.return_value = ORMBook()

            repo.scraping_bulk_insert([domain_book])

            mock_cat_repo.get_or_create_by_name.assert_called_once_with("Fiction")

            session.bulk_save_objects.assert_called_once()
            session.commit.assert_called_once()
