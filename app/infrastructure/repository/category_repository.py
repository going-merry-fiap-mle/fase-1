from app.domain.models import Category
from app.port.category_port import ICategoryRepository


class CategoryRepository(ICategoryRepository):

    def get_categories(self) -> list[Category]:
        # aqui deve ser a query sqlalchemy para buscar as categorias únicas do banco
        # Exemplo: session.query(Book.category).distinct().all()
        # Por enquanto, retornando categorias que correspondem aos livros mock
        test_categories = [
            Category(name="Programming"),
            Category(name="Poetry"),
            Category(name="Fiction"),
        ]
        return test_categories
