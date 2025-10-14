from typing import Tuple

from app.domain.models import Category
from app.infrastructure.database import db
from app.port.category_port import ICategoryRepository


class CategoryRepository(ICategoryRepository):

    def get_categories(self, page: int = 1, per_page: int = 10) -> Tuple[list[Category], int]:
        session = db.get_session()
        try:
            query = session.query(Category)
            total = query.count()

            offset = (page - 1) * per_page
            categories = query.offset(offset).limit(per_page).all()

            return categories, total
        finally:
            session.close()

    def get_or_create_category(self, name: str) -> Category:
        session = db.get_session()
        try:
            category = session.query(Category).filter_by(name=name).first()

            if category is None:
                category = Category(name=name)
                session.add(category)
                session.commit()
                session.refresh(category)

            return category
        finally:
            session.close()
