from typing import Optional, Tuple, List
import re
from decimal import Decimal

from app.port.book_port import IBookRepository
from app.infrastructure.model_store import ModelStore


class MLService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository
        self._model_store = ModelStore()

    def _parse_price(self, price_str: Optional[str]) -> Optional[float]:
        """Parse a price value that can be a string, Decimal, int or float into a float.

        Accepts inputs like:
        - "$12.34", "12,34", "12.34"
        - Decimal('12.34')
        - 12 or 12.34
        Returns None when parsing fails or input is falsy.
        """
        if price_str is None:
            return None

        # If value is already numeric, convert directly
        if isinstance(price_str, (int, float, Decimal)):
            try:
                return float(price_str)
            except Exception:
                return None

        # Otherwise assume string-like
        s = str(price_str).strip()
        if s == "":
            return None

        # normalize common non-digit characters
        s = s.replace('\xa0', ' ')
        s = s.replace(',', '.')

        # extract first numeric-like sequence
        match = re.search(r"\d+[\d.]*", s)
        if not match:
            return None
        try:
            return float(match.group(0))
        except ValueError:
            return None

    def _availability_flag(self, availability: Optional[str]) -> int:
        if not availability:
            return 0
        return 1 if "in stock" in availability.lower() or "disponível" in availability.lower() else 0

    def _image_present(self, image_url: Optional[str]) -> int:
        return 1 if image_url and image_url.strip() != "" else 0

    def build_features_from_book(self, book) -> dict:
        # book is expected to be a domain model with attributes similar to other controllers
        price_num = self._parse_price(getattr(book, 'price', None) or None)
        rating = getattr(book, 'rating', None)
        availability = getattr(book, 'availability', '')
        image_url = getattr(book, 'image_url', '')

        # category may be an object with name or a string
        category = getattr(book, 'category', None)
        if hasattr(category, 'name'):
            category_name = category.name
        else:
            category_name = category or ""

        title = getattr(book, 'title', None)

        return {
            "id": str(getattr(book, 'id', '')),
            "price_num": price_num,
            "rating": rating,
            "availability_flag": self._availability_flag(availability),
            "category": category_name,
            "image_present": self._image_present(image_url),
            "title": title,
        }

    def get_features(self, page: int = 1, per_page: int = 10, category: Optional[str] = None) -> Tuple[List[dict], int]:
        books, total = self._book_repository.get_books(page, per_page)
        items = []
        for book in books:
            # if category filter provided, compare normalized names
            if category:
                cat = getattr(book, 'category', None)
                name = cat.name if hasattr(cat, 'name') else (cat or '')
                if name.lower() != category.lower():
                    continue
            items.append(self.build_features_from_book(book))

        return items, total

    def get_feature_manifest(self) -> dict:
        """Return a manifest describing the features produced by the pipeline.

        Manifest fields:
          - name: feature name
          - dtype: string description of type (numeric/categorical/text)
          - nullable: whether feature can be null
          - description: short description
        """
        manifest = {
            "feature_version": "v1",
            "features": [
                {"name": "id", "dtype": "string", "nullable": False, "description": "Unique book id"},
                {"name": "price_num", "dtype": "float", "nullable": True, "description": "Normalized price as float"},
                {"name": "rating", "dtype": "int", "nullable": True, "description": "Numeric rating (1-5)"},
                {"name": "availability_flag", "dtype": "int", "nullable": False, "description": "Binary flag: 1 if available"},
                {"name": "category", "dtype": "string", "nullable": False, "description": "Category name as string (to be encoded)"},
                {"name": "image_present", "dtype": "int", "nullable": False, "description": "1 if image_url present"},
                {"name": "title", "dtype": "string", "nullable": True, "description": "Book title (raw text)"},
            ],
        }
        return manifest

    def get_training_data(self, page: int = 1, per_page: int = 10, label: str = "rating", sample: float | None = None, seed: int | None = None) -> tuple[list[dict], int]:
        """Build training rows by combining features and the requested label.

        Returns a tuple (rows, total) where rows is a list of dicts with feature columns plus the label column named as requested.
        Raises ValueError if the requested label is not present in the book objects.
        """
        books, total = self._book_repository.get_books(page, per_page)
        rows: list[dict] = []

        # quick check for label existence on first book
        if books:
            if not hasattr(books[0], label):
                # label could be nested (e.g., category.name) not supported here
                raise ValueError(f"Label '{label}' not found in book records")

        for book in books:
            features = self.build_features_from_book(book)
            # get label value
            label_val = getattr(book, label, None)
            # attach label under the name requested
            features[label] = label_val
            rows.append(features)

        # apply sampling if requested (sample as fraction 0-1 or integer count)
        if sample is not None and rows:
            import random

            rng = random.Random(seed)

            if 0 < sample < 1:
                k = max(1, int(len(rows) * sample))
                rows = rng.sample(rows, k)
            elif sample >= 1:
                # treat as absolute count
                k = min(int(sample), len(rows))
                rows = rng.sample(rows, k)

        return rows, total

    def predict(self, instances: list[dict], model_version: str | None = None) -> list[dict]:
        """Prepare instances and run model prediction.

        Accepts a list of dicts where each dict can contain either already-engineered features
        (price_num, rating, availability_flag, category, image_present, title) or raw fields
        (price, availability, image_url). Returns a list of prediction dicts with keys:
          - input_index: index in the input list
          - prediction: model output
          - score: confidence/score (when available)
          - model_version: the model version used
        """
        # normalize instances to feature dicts expected by models
        normalized = []
        for inst in instances:
            # price_num resolution
            price_num = None
            if inst.get('price_num') is not None:
                price_num = inst.get('price_num')
            elif inst.get('price') is not None:
                price_num = self._parse_price(inst.get('price'))

            # rating
            rating = inst.get('rating', None)

            # availability_flag
            if inst.get('availability_flag') is not None:
                availability_flag = inst.get('availability_flag')
            else:
                availability_flag = self._availability_flag(inst.get('availability', None))

            # image_present
            if inst.get('image_present') is not None:
                image_present = inst.get('image_present')
            else:
                image_present = self._image_present(inst.get('image_url', None))

            category = inst.get('category', '')
            title = inst.get('title', None)

            normalized.append({
                'price_num': price_num,
                'rating': rating,
                'availability_flag': availability_flag,
                'category': category,
                'image_present': image_present,
                'title': title,
            })

        # load model
        model = self._model_store.load_model(model_version)

        # model is expected to implement predict(list[dict]) -> list[dict] with keys prediction and score
        results = model.predict(normalized)

        # attach metadata
        out = []
        for idx, res in enumerate(results):
            entry = {
                'input_index': idx,
                'prediction': res.get('prediction'),
                'score': res.get('score'),
                'model_version': model_version or 'default',
            }
            out.append(entry)

        return out
