
import joblib
from pathlib import Path
from typing import Any, Dict
import numpy as np

from app.utils.logger import AppLogger


class MLModelLoader:
    _instance = None
    _models: Dict[str, Any] = {}
    _encoders: Dict[str, Any] = {}
    _metadata: Dict[str, Any] = {}
    _cache: Dict[str, Any] = {}
    _is_initialized = False
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self._logger = AppLogger(__name__)
            self._load_models()
            self._is_initialized = True

    def _load_models(self):
        self._logger.info("=" * 60)
        self._logger.info("[ML] MODEL LOADER - Inicializando...")
        self._logger.info("=" * 60)

        project_root = Path(__file__).resolve().parent.parent.parent
        models_dir = project_root / "models"

        if not models_dir.exists():
            self._logger.warning("Directory 'models/' not found")
            self._logger.info("HINT: Run: python ml_training/train_model.py")
            self._logger.info("=" * 60)
            return

        self._load_rating_model(models_dir)
        self._load_encoders(models_dir)
        self._load_metadata(models_dir)

        self._logger.info("=" * 60)
        if self._models:
            self._logger.info(f"{len(self._models)} model(s) loaded successfully!")
        else:
            self._logger.warning("No models loaded")
            self._logger.info("HINT: Run: python ml_training/train_model.py")
        self._logger.info("=" * 60)

    def _load_rating_model(self, models_dir: Path):
        model_path = models_dir / "rating_classifier_v1.pkl"

        if model_path.exists():
            try:
                self._models['rating'] = joblib.load(model_path)
                self._logger.info(f"   [OK] Model 'rating' loaded: {model_path.name}")
            except Exception as e:
                self._logger.error(f"   Error loading model 'rating': {str(e)}")
        else:
            self._logger.warning(f"   Model 'rating' not found: {model_path}")

    def _load_encoders(self, models_dir: Path):
        encoders_path = models_dir / "encoders_v1.pkl"

        if encoders_path.exists():
            try:
                self._encoders = joblib.load(encoders_path)
                self._logger.info(f"   [OK] Encoders loaded: {encoders_path.name}")
            except Exception as e:
                self._logger.error(f"   Error loading encoders: {str(e)}")
        else:
            self._logger.warning(f"   Encoders not found: {encoders_path}")

    def _load_metadata(self, models_dir: Path):
        metadata_path = models_dir / "model_metadata.pkl"

        if metadata_path.exists():
            try:
                self._metadata = joblib.load(metadata_path)
                self._logger.info(f"   [OK] Metadata loaded: {metadata_path.name}")
            except Exception as e:
                self._logger.error(f"   Error loading metadata: {str(e)}")

    def get_model(self, model_type: str) -> Any | None:
        return self._models.get(model_type)

    def get_encoder(self, encoder_name: str) -> Any | None:
        return self._encoders.get(encoder_name)

    def is_loaded(self, model_type: str) -> bool:
        return model_type in self._models

    def get_metadata(self) -> Dict[str, Any]:
        return self._metadata

    def get_available_models(self) -> list:
        return list(self._models.keys())

    def predict_with_cache(
        self,
        model_type: str,
        features: np.ndarray,
        cache_key: str | None = None
    ) -> Any | None:
        if not self.is_loaded(model_type):
            return None

        if cache_key and cache_key in self._cache:
            return self._cache[cache_key]

        model = self.get_model(model_type)
        if model is None:
            return None

        prediction = model.predict(features)

        if cache_key:
            self._cache[cache_key] = prediction

        return prediction

    def clear_cache(self):
        self._cache.clear()
        self._logger.info("Predictions cache cleared")

    def reload_models(self):
        self._logger.info("Reloading models...")
        self._models.clear()
        self._encoders.clear()
        self._metadata.clear()
        self._cache.clear()
        self._load_models()


ml_loader = MLModelLoader()


def get_model(model_type: str):
    return ml_loader.get_model(model_type)


def get_encoder(encoder_name: str):
    return ml_loader.get_encoder(encoder_name)


def is_model_loaded(model_type: str) -> bool:
    return ml_loader.is_loaded(model_type)


def get_available_models() -> list:
    return ml_loader.get_available_models()
