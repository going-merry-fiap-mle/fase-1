from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    id: str
    title: str
    price: str
    rating: Optional[int]
    availability: str
    category: str
    image_url: str
