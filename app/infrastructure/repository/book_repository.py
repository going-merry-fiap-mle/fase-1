from decimal import Decimal
from uuid import UUID
import math

from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.models.category import Category
from app.infrastructure.session_manager import get_session
from app.port.book_port import IBookRepository
from sqlalchemy import func


class BookRepository(IBookRepository):

    def get_books(self, page: int | None = 1, per_page: int | None = 10, category: str | None = None) -> tuple[list[DomainBook], int]:
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

    def get_books_by_price(self, page: int = 1, per_page: int = 10, min_price: Decimal = Decimal('0'), max_price: Decimal = Decimal('Infinity')) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            filters = [Book.price >= min_price]
            if not math.isinf(max_price):
                filters.append(Book.price <= max_price)

            filtered_query = session.query(Book).filter(*filters)
            total = filtered_query.count()

            offset = (page - 1) * per_page
            books_orm = (
                filtered_query
                .offset(offset)
                .limit(per_page)
                .all()
            )

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total
         
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
