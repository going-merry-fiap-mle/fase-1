from typing import Optional
from pydantic import BaseModel


class ScrapingBase(BaseModel):
    title: str
    price: str
    rating: Optional[int]
    availability: str
    category: str
    image_url: str


class Book(ScrapingBase):
    pass
