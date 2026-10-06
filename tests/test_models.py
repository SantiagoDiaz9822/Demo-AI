import json

import pytest
from pydantic import ValidationError

from models import ProductRequirements


def test_creates_complete_product_requirements() -> None:
    requirements = ProductRequirements(
        category=" Monitor ",
        brand=" Samsung ",
        max_price=500,
        size_inches=27,
        use_case=" Programming ",
    )

    assert requirements.category == "monitor"
    assert requirements.brand == "Samsung"
    assert requirements.max_price == 500
    assert requirements.size_inches == 27
    assert requirements.use_case == "programming"


def test_optional_values_default_to_none() -> None:
    requirements = ProductRequirements(category="laptop")

    assert requirements.brand is None
    assert requirements.max_price is None
    assert requirements.size_inches is None
    assert requirements.use_case is None


def test_serializes_to_json() -> None:
    requirements = ProductRequirements(category="headphones", brand="Sony", max_price=200)

    assert json.loads(requirements.model_dump_json()) == {
        "category": "headphones",
        "brand": "Sony",
        "max_price": 200.0,
        "size_inches": None,
        "use_case": None,
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [("max_price", 0), ("max_price", -1), ("size_inches", 0)],
)
def test_rejects_non_positive_numeric_values(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        ProductRequirements.model_validate({"category": "monitor", field: value})


def test_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ProductRequirements.model_validate({"category": "monitor", "color": "black"})
