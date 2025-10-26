from pydantic import BaseModel
from typing import Optional


class FeatureOut(BaseModel):
    id: str
    price_num: Optional[float]
    rating: Optional[int]
    availability_flag: int
    category: str
    image_present: int
    # raw fields for traceability
    title: Optional[str]


class FeaturesResponse(BaseModel):
    items: list[FeatureOut]
    total: int
    page: int
    per_page: int
    total_pages: int
    feature_version: str = "v1"


class FeaturesQueryParams(BaseModel):
    page: int = 1
    per_page: int = 10
    category: Optional[str] = None
