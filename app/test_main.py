import datetime
import pytest
from unittest.mock import patch
from app.main import outdated_products


@pytest.fixture
def products() -> list:
    return [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160
        }
    ]


def test_outdated_products_expired_date(products: list) -> None:
    with patch("app.main.datetime.date", wraps=datetime.date) as mock_date:
        mock_date.today = lambda: datetime.date(2022, 2, 5)
        result = outdated_products(products)
        assert result == ["duck"]


def test_outdated_products_not_expired(products: list) -> None:
    with patch("app.main.datetime.date", wraps=datetime.date) as mock_date:
        mock_date.today = lambda: datetime.date(2022, 2, 1)
        result = outdated_products(products)
        assert result == []


def test_outdated_products_on_expiry_date(products: list) -> None:
    with patch("app.main.datetime.date", wraps=datetime.date) as mock_date:
        mock_date.today = lambda: datetime.date(2022, 2, 10)
        result = outdated_products(products)
        assert result == ["chicken", "duck"]


def test_outdated_products_with_future_date(products: list) -> None:
    with patch("app.main.datetime.date", wraps=datetime.date) as mock_date:
        mock_date.today = lambda: datetime.date(2022, 2, 15)
        result = outdated_products(products)
        assert result == ["salmon", "chicken", "duck"]


def test_outdated_products_with_yesterday_date(products: list) -> None:
    with patch("app.main.datetime.date", wraps=datetime.date) as mock_date:
        mock_date.today = lambda: datetime.date(2022, 2, 2)
        result = outdated_products(products)
        assert result == ["duck"]
