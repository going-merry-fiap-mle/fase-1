import uuid
from decimal import Decimal
from typing import Optional

from app.domain.models.category_domain_model import Category


class Book:
    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        price: Decimal,
        rating: Optional[int],
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
