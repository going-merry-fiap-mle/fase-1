from app.domain.models.category_domain_model import Category as DomainCategory
from app.infrastructure.models.category import Category
from app.infrastructure.session_manager import get_session


class CategoryRepository:

    def get_or_create_by_name(self, name: str) -> DomainCategory:
        with get_session() as session:
            category_orm = session.query(Category).filter(Category.name == name).first()

            if category_orm is None:
                domain_category = DomainCategory(name=name)
                category_orm = Category.from_domain(domain_category)
                session.add(category_orm)

            return category_orm.to_domain()
