from pydantic import BaseModel


class CategoryStats(BaseModel):
    name: str
    book_count: int
    min_price: float | None
    max_price: float | None
    avg_price: float | None
