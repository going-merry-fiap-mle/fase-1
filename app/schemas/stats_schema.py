from pydantic import BaseModel
from typing import Dict, Optional


class OverviewStats(BaseModel):
    total_books: int
    avg_price: Optional[float]
    rating_distribution: Dict[str, int]

