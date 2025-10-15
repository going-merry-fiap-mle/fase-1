from pydantic import BaseModel


class BookBase(BaseModel):
    id: str
    title: str
    price: str
    rating: int | None
    availability: str
    category: str
    image_url: str
