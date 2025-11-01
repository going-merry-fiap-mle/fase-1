from app.domain.models.category_domain_model import Category as DomainCategory
from app.infrastructure.models.category import Category
from app.infrastructure.session_manager import get_session
from app.port.category_port import ICategoryRepository

from sqlalchemy import func
from app.infrastructure.models.book import Book


class CategoryRepository(ICategoryRepository):

    def get_categories(self, page: int = 1, per_page: int = 10) -> tuple[list[DomainCategory], int]:
        with get_session() as session:
            total = session.query(Category).count()

            offset = (page - 1) * per_page
            categories_orm = (
                session.query(Category)
                .offset(offset)
                .limit(per_page)
                .all()
            )

            domain_categories = [category.to_domain() for category in categories_orm]

            return domain_categories, total

    def get_or_create_category(self, name: str) -> DomainCategory:
        with get_session() as session:
            category_orm = session.query(Category).filter(Category.name == name).first()

            if category_orm is None:
                domain_category = DomainCategory(name=name)
                category_orm = Category.from_domain(domain_category)
                session.add(category_orm)
                session.flush()

            return category_orm.to_domain()

    def get_or_create_by_name(self, name: str) -> DomainCategory:
        return self.get_or_create_category(name)

    def get_category_stats(self, page: int = 1, per_page: int = 10) -> tuple[list[dict], int]:
        with get_session() as session:
            total = session.query(Category).count()

            offset = (page - 1) * per_page
            rows = (
                session.query(
                    Category.name,
                    func.count(Book.id).label("book_count"),
                    func.min(Book.price).label("min_price"),
                    func.max(Book.price).label("max_price"),
                    func.avg(Book.price).label("avg_price"),
                )
                .outerjoin(Book, Book.category_id == Category.id)
                .group_by(Category.name)
                .offset(offset)
                .limit(per_page)
                .all()
            )

            items: list[dict] = []
            for row in rows:
                name = row[0]
                book_count = int(row[1] or 0)
                min_price = float(row[2]) if row[2] is not None else None
                max_price = float(row[3]) if row[3] is not None else None
                avg_price = round(float(row[4]), 2) if row[4] is not None else None

                items.append({
                    "name": name,
                    "book_count": book_count,
                    "min_price": min_price,
                    "max_price": max_price,
                    "avg_price": avg_price,
                })

            return items, total
