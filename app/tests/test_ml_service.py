from types import SimpleNamespace
import pytest
from app.services.ml_service import MLService


class FakeRepo:
    def __init__(self, books, total=0):
        self._books = books
        self._total = total

    def get_books(self, page=None, per_page=None, category=None):
        return self._books, self._total


def make_book(**kwargs):
    return SimpleNamespace(**kwargs)


def test_parse_price_various_formats():
    svc = MLService(book_repository=FakeRepo([]))

    # None and empty
    assert svc._parse_price(None) is None
    assert svc._parse_price("") is None

    # numeric types
    assert svc._parse_price(5) == 5.0
    assert svc._parse_price(3.2) == 3.2

    from decimal import Decimal

    assert svc._parse_price(Decimal("12.50")) == 12.5
    assert svc._parse_price("51,77") == 51.77
    assert svc._parse_price("$12.99") == 12.99
    assert svc._parse_price("  7.5 ") == 7.5
    assert svc._parse_price("12\xa034") == 12.0
    assert svc._parse_price("abc") is None


def test_availability_and_image_present():
    svc = MLService(book_repository=FakeRepo([]))

    assert svc._availability_flag(None) == 0
    assert svc._availability_flag("") == 0
    assert svc._availability_flag("Out of stock") == 0
    assert svc._availability_flag("In Stock") == 1
    assert svc._availability_flag("Disponível agora") == 1
    assert svc._image_present(None) == 0
    assert svc._image_present("") == 0
    assert svc._image_present("   ") == 0
    assert svc._image_present("http://example.com/img.png") == 1


def test_build_features_with_category_object_and_string():
    svc = MLService(book_repository=FakeRepo([]))

    cat_obj = SimpleNamespace(name="Poetry")
    book1 = make_book(id="1", price="10.00", rating=4, availability="In stock", image_url="u", category=cat_obj, title="T")
    features1 = svc.build_features_from_book(book1)
    assert features1["category"] == "Poetry"
    assert features1["availability_flag"] == 1
    assert features1["image_present"] == 1
    assert features1["price_num"] == 10.0

    book2 = make_book(id="2", price=None, rating=None, availability="", image_url="", category="Fiction", title=None)
    features2 = svc.build_features_from_book(book2)
    assert features2["category"] == "Fiction"
    assert features2["availability_flag"] == 0
    assert features2["image_present"] == 0
    assert features2["price_num"] is None


def test_get_features_uses_repository_and_returns_total():
    book = make_book(id="1", price="1.99", rating=5, availability="In stock", image_url="u", category="C", title="Title")
    repo = FakeRepo([book], total=42)
    svc = MLService(book_repository=repo)

    items, total = svc.get_features(page=1, per_page=10, category=None)
    assert total == 42
    assert isinstance(items, list)
    assert items[0]["id"] == "1"
    assert items[0]["price_num"] == 1.99


def test_get_feature_manifest_has_expected_structure():
    svc = MLService(book_repository=FakeRepo([]))
    manifest = svc.get_feature_manifest()
    assert manifest["feature_version"] == "v1"
    names = [f["name"] for f in manifest["features"]]
    assert "price_num" in names
    assert "image_present" in names


def test_get_training_data_label_missing_raises():
    book = make_book(id="1", price="1.00", rating=5)
    repo = FakeRepo([book], total=1)
    svc = MLService(book_repository=repo)

    with pytest.raises(ValueError):
        svc.get_training_data(label="nonexistent")


def test_get_training_data_returns_rows_and_total_and_includes_label():
    books = [
        make_book(id=str(i), price=f"{i}.00", rating=i % 5 + 1, availability="In stock", image_url="u", category="C", title=f"T{i}")
        for i in range(1, 6)
    ]
    repo = FakeRepo(books, total=5)
    svc = MLService(book_repository=repo)

    rows, total = svc.get_training_data()
    assert total == 5
    assert len(rows) == 5
    for r, b in zip(rows, books):
        assert r["rating"] == b.rating


def test_get_training_data_sampling_fraction_and_seed_deterministic():
    books = [make_book(id=str(i), price=f"{i}.00", rating=i, availability="In stock", image_url="u", category="C", title=f"T{i}") for i in range(10)]
    repo = FakeRepo(books, total=10)
    svc = MLService(book_repository=repo)

    rows_a, _ = svc.get_training_data(sample=0.3, seed=123)
    rows_b, _ = svc.get_training_data(sample=0.3, seed=123)
    assert len(rows_a) == 3
    assert rows_a == rows_b  # deterministic with same seed

    rows_c, _ = svc.get_training_data(sample=0.3, seed=999)
    assert rows_c != rows_a


def test_get_training_data_sampling_absolute_and_bounds():
    books = [make_book(id=str(i), price=f"{i}.00", rating=i, availability="In stock", image_url="u", category="C", title=f"T{i}") for i in range(5)]
    repo = FakeRepo(books, total=5)
    svc = MLService(book_repository=repo)

    rows, _ = svc.get_training_data(sample=2, seed=1)
    assert len(rows) == 2

    rows_all, _ = svc.get_training_data(sample=10, seed=1)
    assert len(rows_all) == 5


def test_get_training_data_empty_books_returns_empty():
    repo = FakeRepo([], total=0)
    svc = MLService(book_repository=repo)

    rows, total = svc.get_training_data()
    assert rows == []
    assert total == 0

