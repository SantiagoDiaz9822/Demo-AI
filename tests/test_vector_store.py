from pathlib import Path

from models import RAGDocument
from rag.vector_store import ProductVectorStore


def test_persists_and_searches_documents(tmp_path: Path) -> None:
    documents = [
        RAGDocument(
            text="Product: Programming Monitor",
            metadata={
                "product_id": "monitor_1",
                "product_name": "Programming Monitor",
                "category": "monitor",
                "price_usd": 400,
            },
        ),
        RAGDocument(
            text="Product: Wireless Headphones",
            metadata={
                "product_id": "headphones_1",
                "product_name": "Wireless Headphones",
                "category": "headphones",
                "price_usd": 100,
            },
        ),
    ]
    store_path = tmp_path / "chroma"
    ProductVectorStore(store_path).replace(documents, [[1.0, 0.0], [0.0, 1.0]])

    reopened = ProductVectorStore(store_path)
    results = reopened.search([1.0, 0.0], top_k=1)

    assert reopened.count() == 2
    assert results[0].metadata["product_id"] == "monitor_1"
    assert results[0].distance == 0
