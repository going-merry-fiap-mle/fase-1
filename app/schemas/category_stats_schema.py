from pydantic import BaseModel
from typing import Optional


class CategoryStats(BaseModel):
    name: str
    book_count: int
    min_price: Optional[float]
    max_price: Optional[float]
    avg_price: Optional[float]
