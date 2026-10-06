"""Indexación independiente: ``python -m rag.ingest``."""

from pathlib import Path

from rag.document_builder import product_to_document
from rag.embeddings import EmbeddingError, embed_documents, embedding_model_name
from rag.loader import ProductLoadError, load_products
from rag.vector_store import ProductVectorStore, VectorStoreError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "products.xlsx"
DEFAULT_STORE_PATH = PROJECT_ROOT / "storage" / "vector_store"


# Ejecuta la carga, transformación, vectorización y persistencia del dataset.
def ingest(
    data_path: str | Path = DEFAULT_DATA_PATH,
    store_path: str | Path = DEFAULT_STORE_PATH,
) -> int:
    """Carga, transforma, vectoriza y persiste todos los productos."""

    products = load_products(data_path)
    print(f"Products loaded: {len(products)}")
    documents = [product_to_document(product) for product in products]
    print(f"Documents created: {len(documents)}")
    embeddings = embed_documents([document.text for document in documents])
    print(f"Embeddings generated: {len(embeddings)} ({embedding_model_name()})")
    ProductVectorStore(store_path).replace(documents, embeddings)
    print("Vector store persisted successfully.")
    return len(documents)


# Ofrece un punto de entrada de consola con manejo amigable de errores.
def main() -> None:
    try:
        ingest()
    except (ProductLoadError, EmbeddingError, VectorStoreError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error


if __name__ == "__main__":
    main()
