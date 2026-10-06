from types import SimpleNamespace

import rag.embeddings as embeddings


def test_embeds_documents_without_real_provider(monkeypatch) -> None:
    captured = {}

    class FakeClient:
        def __init__(self, *, host: str) -> None:
            captured["host"] = host

        def embed(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(embeddings=[[1.0, 0.0], [0.0, 1.0]])

    monkeypatch.setattr(embeddings, "Client", FakeClient)
    monkeypatch.setattr(embeddings, "load_dotenv", lambda: None)
    monkeypatch.setenv("OLLAMA_EMBEDDING_MODEL", "test-embed")

    result = embeddings.embed_documents(["one", "two"])

    assert result == [[1.0, 0.0], [0.0, 1.0]]
    assert captured["model"] == "test-embed"
    assert captured["input"] == ["one", "two"]
