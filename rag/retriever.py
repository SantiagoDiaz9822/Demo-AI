"""Operaciones de alto nivel para el retrieval fijo del pipeline."""

from pathlib import Path

from models import RetrievedProduct
from rag.embeddings import embed_query
from rag.vector_store import ProductVectorStore

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE_PATH = PROJECT_ROOT / "storage" / "vector_store"


# Vectoriza la consulta y recupera los productos semánticamente más cercanos.
def retrieve_relevant_products(
    query: str,
    top_k: int = 4,
    store_path: str | Path = DEFAULT_STORE_PATH,
) -> list[RetrievedProduct]:
    """Ejecuta semantic search directamente; no es una Tool del LLM."""

    query_embedding = embed_query(query)
    return ProductVectorStore(store_path).search(query_embedding, top_k)


# Une los documentos recuperados para formar el contexto de generación.
def build_context(products: list[RetrievedProduct]) -> str:
    """Concatena los productos recuperados sin agregar hechos nuevos."""

    return "\n\n".join(
        f"[Retrieved product {index}]\n{product.text}"
        for index, product in enumerate(products, start=1)
    )
