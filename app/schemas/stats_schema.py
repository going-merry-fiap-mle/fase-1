from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_books: int
    avg_price: float | None
    rating_distribution: dict[str, int]

