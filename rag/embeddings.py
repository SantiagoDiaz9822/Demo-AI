"""Capa pequeña de embeddings con el mismo proveedor local de la V0."""

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

DEFAULT_EMBEDDING_MODEL = "nomic-embed-text:latest"
DEFAULT_HOST = "http://localhost:11434"


# Representa errores al solicitar o validar embeddings de Ollama.
class EmbeddingError(RuntimeError):
    """No fue posible producir embeddings para el pipeline."""


# Obtiene el modelo de embeddings configurado o devuelve el predeterminado.
def embedding_model_name() -> str:
    load_dotenv()
    return os.getenv("OLLAMA_EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL


# Genera en lote un embedding por cada documento que se indexará.
def embed_documents(texts: list[str]) -> list[list[float]]:
    """Genera un vector por texto mediante el endpoint de embeddings de Ollama."""

    if not texts:
        return []
    if any(not text.strip() for text in texts):
        raise ValueError("Los textos para embeddings no pueden estar vacíos.")

    load_dotenv()
    host = os.getenv("OLLAMA_HOST") or DEFAULT_HOST
    model = embedding_model_name()
    client = Client(host=host)
    try:
        response = client.embed(model=model, input=texts)
    except ConnectionError as error:
        raise EmbeddingError(
            "No se pudo conectar con Ollama para generar embeddings."
        ) from error
    except ResponseError as error:
        if error.status_code == 404:
            raise EmbeddingError(
                f"No se encontró el modelo de embeddings '{model}'. "
                f"Instalalo con: ollama pull {model}"
            ) from error
        raise EmbeddingError("Ollama no pudo generar los embeddings.") from error

    embeddings = [list(vector) for vector in response.embeddings]
    if len(embeddings) != len(texts):
        raise EmbeddingError("Ollama devolvió una cantidad inesperada de embeddings.")
    return embeddings


# Genera el embedding de una consulta para compararlo con los documentos.
def embed_query(text: str) -> list[float]:
    """Genera el vector de una consulta con el mismo modelo de la ingesta."""

    if not text.strip():
        raise ValueError("La consulta para retrieval no puede estar vacía.")
    return embed_documents([text])[0]
