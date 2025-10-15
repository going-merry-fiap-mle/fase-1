import math
from typing import Generic, TypeVar
from pydantic import BaseModel, Field, computed_field

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Número da página (mínimo: 1)")
    per_page: int = Field(default=10, ge=1, le=100, description="Itens por página (mínimo: 1, máximo: 100)")


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total_items: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return math.ceil(self.total_items / self.per_page) if self.per_page > 0 else 0


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta
