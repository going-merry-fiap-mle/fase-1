from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class PredictionBase(BaseModel):
    id: str | None = None
    book_id: str
    prediction_type: Literal["rating", "category", "price", "recommendation"]
    predicted_value: str | None = None
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    model_version: str | None = Field(None, min_length=1)
    metadata: dict | None = None
    created_at: datetime | None = None

    @field_validator("predicted_value")
    @classmethod
    def validate_predicted_value(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("predicted_value cannot be empty string")
        return v

    @field_validator("model_version")
    @classmethod
    def validate_model_version(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("model_version cannot be empty string")
        return v

    @model_validator(mode="after")
    def validate_model_version_with_predicted_value(self):
        if self.predicted_value is not None and self.model_version is None:
            raise ValueError("model_version is required when predicted_value is provided")
        return self


class MLPredictionResponse(BaseModel):
    book_id: str
    book_title: str
    predicted_value: str
    predicted_label: str
    confidence: float
    features_used: dict
    model_version: str
    from_cache: bool


class MLExecutionResponse(BaseModel):
    prediction: MLPredictionResponse
    saved_prediction_id: str


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
