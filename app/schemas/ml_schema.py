from pydantic import BaseModel

class FeatureOut(BaseModel):
    id: str
    price_num: float | None
    rating: int | None
    availability_flag: int
    category: str
    image_present: int
    title: str | None


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
    category: str | None = None
