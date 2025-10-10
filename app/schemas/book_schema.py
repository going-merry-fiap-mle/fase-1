from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    price: str
    rating: int
    availability: str
    category: str
    image: str
