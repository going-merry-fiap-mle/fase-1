from app.infrastructure.adapters.book_adapter import BookAdapter
from app.services.ml_service import MLService
from app.schemas.ml_schema import FeaturesResponse, FeatureOut


class MLController:

    def call_controller(self, page: int = 1, per_page: int = 10, category: str | None = None) -> FeaturesResponse:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)

        items, total = ml_service.get_features(page=page, per_page=per_page, category=category)

        items_dto = [FeatureOut(**item) for item in items]

        return FeaturesResponse(items=items_dto, total=total, page=page, per_page=per_page)

    def call_manifest(self) -> dict:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        return ml_service.get_feature_manifest()

    def call_training_data(self, page: int = 1, per_page: int = 10, label: str = "rating", sample: float | None = None) -> tuple[list[dict], int]:
        """Return training rows and total count using MLService.get_training_data."""
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        rows, total = ml_service.get_training_data(page=page, per_page=per_page, label=label, sample=sample)
        return rows, total

    def call_training_data(self, page: int = 1, per_page: int = 10, label: str = "rating", sample: float | None = None, seed: int | None = None) -> tuple[list[dict], int]:
        """Return training rows and total count using MLService.get_training_data with optional seed."""
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        rows, total = ml_service.get_training_data(page=page, per_page=per_page, label=label, sample=sample, seed=seed)
        return rows, total

    def call_predict(self, instances: list[dict], model_version: str | None = None) -> list[dict]:
        """Run predictions for given instances via MLService.predict."""
        # For prediction we don't need BookAdapter, but MLService expects one in constructor; pass adapter
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        return ml_service.predict(instances=instances, model_version=model_version)
