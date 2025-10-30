from decimal import Decimal
from uuid import UUID

from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.models.category import Category
from app.infrastructure.session_manager import get_session
from app.port.book_port import IBookRepository
from sqlalchemy import func
from typing import Optional
class BookRepository(IBookRepository):

    def get_books(self, page: Optional[int] = 1, per_page: Optional[int] = 10, category: Optional[str] = None) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            query = session.query(Book)

            if category:
                cat_name = category.strip().lower()
                query = query.join(Category).filter(func.lower(Category.name) == cat_name)

            total = query.count()

            if per_page is None:
                books_orm = query.all()
            else:
                offset = ((page or 1) - 1) * per_page
                books_orm = (
                    query
                    .offset(offset)
                    .limit(per_page)
                    .all()
                )

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total

    def search_books(
        self,
        title: str | None = None,
        category: str | None = None,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            query = session.query(Book).join(Category)

            if title:
                query = query.filter(Book.title.ilike(f"%{title}%"))
            if category:
                query = query.filter(Category.name.ilike(f"%{category}%"))

            total = query.count()

            offset = (page - 1) * per_page
            books_orm = query.offset(offset).limit(per_page).all()

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total

    def get_top_rated_books(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            query = session.query(Book).order_by(Book.rating.desc(), Book.title)

            total = query.count()

            offset = (page - 1) * per_page
            books_orm = query.offset(offset).limit(per_page).all()

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total

    def create_book(
        self,
        title: str,
        price: str,
        rating: int | None,
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> DomainBook:
        with get_session() as session:
            book_db = Book(
                title=title,
                price=Decimal(price.replace('£', '').replace('€', '')),
                availability=availability,
                category_id=category_id,
                image_url=image_url,
                rating=rating,
            )

            session.add(book_db)
            session.flush()

            return book_db.to_domain()

    def get_overview_stats(self) -> dict:
        with get_session() as session:
            total = session.query(func.count(Book.id)).scalar() or 0

            avg_price_dec = session.query(func.avg(Book.price)).scalar()
            avg_price = round(float(avg_price_dec), 2) if avg_price_dec is not None else None

            rows = session.query(Book.rating, func.count(Book.id)).group_by(Book.rating).all()

            rating_distribution: dict[str, int] = {}
            for rating, count in rows:
                key = str(rating) if rating is not None else "unknown"
                rating_distribution[key] = int(count)

            return {
                "total_books": int(total),
                "avg_price": avg_price,
                "rating_distribution": rating_distribution,
            }
