from app.domain.models.category_domain_model import Category as DomainCategory
from app.infrastructure.models.category import Category
from app.infrastructure.session_manager import get_session
from app.port.category_port import ICategoryRepository


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
