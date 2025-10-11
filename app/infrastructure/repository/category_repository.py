from app.domain.models import Category
from app.port.category_port import ICategoryRepository


class CategoryRepository(ICategoryRepository):

    def get_categories(self) -> list[Category]:
        # aqui deve ser a query sqlalchemy para buscar as categorias únicas do banco
        # Por enquanto, retornando algumas categorias de exemplo
        test_categories = [
            Category(name="Poetry"),
            Category(name="Fiction"),
            Category(name="Science"),
        ]
        return test_categories
