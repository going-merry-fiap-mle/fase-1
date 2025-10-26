from app.infrastructure.adapters.book_adapter import BookAdapter
from app.services.ml_service import MLService
from app.schemas.ml_schema import FeatureOut
from app.schemas.pagination_schema import PaginatedResponse, PaginationMeta


class MLController:

    def call_controller(self, page: int = 1, per_page: int = 10, category: str | None = None) -> PaginatedResponse[FeatureOut]:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)

        items, total = ml_service.get_features(page=page, per_page=per_page, category=category)

        items_dto = [FeatureOut(**item) for item in items]

        pagination_meta = PaginationMeta(page=page, per_page=per_page, total_items=total)
        return PaginatedResponse(items=items_dto, pagination=pagination_meta)

    def call_manifest(self) -> dict:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        return ml_service.get_feature_manifest()

    def call_training_data(self, label: str = "rating", sample: float | None = None, seed: int | None = None) -> tuple[list[dict], int]:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        rows, total = ml_service.get_training_data(label=label, sample=sample, seed=seed)
        return rows, total

    def call_predict(self, instances: list[dict], model_version: str | None = None) -> list[dict]:
        book_adapter = BookAdapter()
        ml_service = MLService(book_adapter)
        return ml_service.predict(instances=instances, model_version=model_version)
