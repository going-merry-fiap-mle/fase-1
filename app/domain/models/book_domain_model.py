import uuid
from decimal import Decimal

from app.domain.models.category_domain_model import Category


class Book:
    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        price: Decimal,
        rating: int | None,
        availability: str,
        category: Category,
        image_url: str,
    ) -> None:
        self.id = id
        self.title = title
        self.price = price
        self.rating = rating
        self.availability = availability
        self.category = category
        self.image_url = image_url
