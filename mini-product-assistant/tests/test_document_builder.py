from models import ProductRecord
from rag.document_builder import product_to_document


def test_builds_searchable_text_and_preserves_metadata() -> None:
    product = ProductRecord(
        product_id="monitor_1",
        category="monitor",
        brand="Demo",
        product_name="Monitor One",
        price_usd=300,
        description="A monitor for programming.",
    )

    document = product_to_document(product)

    assert "Product: Monitor One" in document.text
    assert "Category: monitor" in document.text
    assert "Description: A monitor for programming." in document.text
    assert document.metadata["product_id"] == "monitor_1"
    assert document.metadata["price_usd"] == 300


def test_does_not_mix_two_products() -> None:
    first = product_to_document(
        ProductRecord(product_id="one", category="monitor", product_name="First")
    )
    second = product_to_document(
        ProductRecord(product_id="two", category="laptop", product_name="Second")
    )

    assert "Second" not in first.text
    assert "First" not in second.text
