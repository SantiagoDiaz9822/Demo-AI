from pathlib import Path

import rag.ingest as ingest_module


def test_ingest_builds_one_document_and_embedding_per_product(
    monkeypatch, tmp_path: Path
) -> None:
    captured = {}

    monkeypatch.setattr(
        ingest_module,
        "embed_documents",
        lambda texts: [[float(index), 1.0] for index, _ in enumerate(texts)],
    )
    monkeypatch.setattr(ingest_module, "embedding_model_name", lambda: "fake-model")

    class FakeStore:
        def __init__(self, path) -> None:
            captured["path"] = path

        def replace(self, documents, embeddings) -> None:
            captured["documents"] = documents
            captured["embeddings"] = embeddings

    monkeypatch.setattr(ingest_module, "ProductVectorStore", FakeStore)
    data_path = Path(__file__).resolve().parent.parent / "data" / "products.xlsx"

    count = ingest_module.ingest(data_path, tmp_path / "store")

    assert count == 20
    assert len(captured["documents"]) == 20
    assert len(captured["embeddings"]) == 20
