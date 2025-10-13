from pydantic import BaseModel


class ScrapingBase(BaseModel):
    title: str
    price: str
    rating: int
    availability: str
    category: str
    image: str


class Book(BaseModel):
    title: str
    price: str
    rating: int
    availability: str
    category: str
    image_url: str
