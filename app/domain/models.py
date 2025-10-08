from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    title: str
    price: str
    rating: int
    availability: str
    category: str
    image: str
