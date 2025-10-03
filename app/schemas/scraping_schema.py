from pydantic import BaseModel


class ScrapingBase(BaseModel):
    title: str
    price: str
    rating: int
    availability: str
    category: str
    image: str
