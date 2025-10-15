from pydantic import BaseModel


class ScrapingBase(BaseModel):
    title: str
    price: str
    rating: int | None
    availability: str
    category: str
    image_url: str


class Book(ScrapingBase):
    pass
