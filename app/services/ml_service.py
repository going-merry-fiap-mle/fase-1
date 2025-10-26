from typing import Optional, Tuple, List
import re
from decimal import Decimal

from app.port.book_port import IBookRepository


class MLService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository

    def _parse_price(self, price_str: Optional[str]) -> Optional[float]:
        if price_str is None:
            return None

        if isinstance(price_str, (int, float, Decimal)):
            try:
                return float(price_str)
            except Exception:
                return None

        s = str(price_str).strip()
        if s == "":
            return None

        s = s.replace('\xa0', ' ')
        s = s.replace(',', '.')

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
        price_num = self._parse_price(getattr(book, 'price', None) or None)
        rating = getattr(book, 'rating', None)
        availability = getattr(book, 'availability', '')
        image_url = getattr(book, 'image_url', '')

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
        books, total = self._book_repository.get_books(page, per_page, category)
        items = [self.build_features_from_book(book) for book in books]
        return items, total

    def get_feature_manifest(self) -> dict:
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

    def get_training_data(self, label: str = "rating", sample: float | None = None, seed: int | None = None) -> tuple[list[dict], int]:
        books, total = self._book_repository.get_books(page=None, per_page=None)
        rows: list[dict] = []

        if books:
            if not hasattr(books[0], label):
                raise ValueError(f"Label '{label}' not found in book records")

        for book in books:
            features = self.build_features_from_book(book)
            label_val = getattr(book, label, None)
            features[label] = label_val
            rows.append(features)

        if sample is not None and rows:
            import random

            rng = random.Random(seed)

            if 0 < sample < 1:
                k = max(1, int(len(rows) * sample))
                rows = rng.sample(rows, k)
            elif sample >= 1:
                k = min(int(sample), len(rows))
                rows = rng.sample(rows, k)

        return rows, total

