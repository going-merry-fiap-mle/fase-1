from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: str
    name: str
