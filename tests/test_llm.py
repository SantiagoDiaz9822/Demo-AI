import pytest

import llm
from models import ProductRequirements


def test_rejects_empty_input_before_calling_provider() -> None:
    with pytest.raises(ValueError, match="no puede estar vacía"):
        llm.extract_product_requirements("   ")


def test_returns_the_typed_structured_output(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = ProductRequirements(category="monitor", brand="Samsung", max_price=500)
    captured: dict[str, object] = {}

    class FakeClient:
        def __init__(self, *, host: str) -> None:
            captured["host"] = host

        def chat(self, **kwargs: object) -> object:
            captured.update(kwargs)
            message = type("FakeMessage", (), {"content": expected.model_dump_json()})()
            return type("FakeResponse", (), {"message": message})()

    monkeypatch.setattr(llm, "load_dotenv", lambda: None)
    monkeypatch.setattr(llm, "Client", FakeClient)
    monkeypatch.setenv("OLLAMA_HOST", "http://test-host:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "test-model")

    result = llm.extract_product_requirements("Quiero un monitor Samsung")

    assert result == expected
    assert captured["host"] == "http://test-host:11434"
    assert captured["model"] == "test-model"
    assert captured["messages"] == [
        {"role": "system", "content": llm.EXTRACTION_INSTRUCTIONS},
        {"role": "user", "content": "Quiero un monitor Samsung"},
    ]
    assert captured["format"] == ProductRequirements.model_json_schema()
    assert captured["options"] == {"temperature": 0}


def test_reports_an_invalid_structured_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeClient:
        def __init__(self, *, host: str) -> None:
            pass

        def chat(self, **kwargs: object) -> object:
            message = type("FakeMessage", (), {"content": "not-json"})()
            return type("FakeResponse", (), {"message": message})()

    monkeypatch.setattr(llm, "load_dotenv", lambda: None)
    monkeypatch.setattr(llm, "Client", FakeClient)

    with pytest.raises(llm.LLMResponseError, match="no cumple el esquema"):
        llm.extract_product_requirements("Necesito un monitor")
