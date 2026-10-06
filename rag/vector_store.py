"""Adaptador mínimo sobre un vector store Chroma local y persistente."""

from pathlib import Path
from typing import Any

from models import RAGDocument, RetrievedProduct

COLLECTION_NAME = "products"


# Representa errores al crear, abrir o consultar el índice persistido.
class VectorStoreError(RuntimeError):
    """El índice persistido no existe o no se puede consultar."""


# Encapsula las operaciones mínimas de persistencia y búsqueda en Chroma.
class ProductVectorStore:
    """Expone solo las operaciones necesarias para enseñar add/search."""

    # Abre o crea un cliente Chroma persistente en el directorio indicado.
    def __init__(self, persist_directory: str | Path) -> None:
        try:
            import chromadb
        except ImportError as error:
            raise VectorStoreError(
                "Falta Chroma. Instalá las dependencias con: pip install -r requirements.txt"
            ) from error

        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_directory))

    # Sustituye el índice actual por un conjunto completo de documentos y vectores.
    def replace(self, documents: list[RAGDocument], embeddings: list[list[float]]) -> None:
        """Reemplaza el índice completo durante el proceso independiente de ingesta."""

        if len(documents) != len(embeddings):
            raise ValueError("Cada documento debe tener exactamente un embedding.")
        if not documents:
            raise ValueError("No hay documentos para indexar.")

        try:
            self._client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        collection = self._client.create_collection(
            COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        collection.add(
            ids=[str(document.metadata["product_id"]) for document in documents],
            documents=[document.text for document in documents],
            metadatas=[document.metadata for document in documents],
            embeddings=embeddings,
        )

    # Devuelve la cantidad de productos guardados o cero si aún no hay colección.
    def count(self) -> int:
        try:
            return self._client.get_collection(COLLECTION_NAME).count()
        except Exception:
            return 0

    # Recupera los Top K productos con menor distancia coseno a la consulta.
    def search(self, query_embedding: list[float], top_k: int) -> list[RetrievedProduct]:
        """Busca por coseno; una distancia menor representa mayor similitud."""

        if top_k < 1:
            raise ValueError("top_k debe ser mayor o igual a 1.")
        try:
            collection = self._client.get_collection(COLLECTION_NAME)
        except Exception as error:
            raise VectorStoreError(
                "No existe el índice. Ejecutá primero: python -m rag.ingest"
            ) from error
        if collection.count() == 0:
            raise VectorStoreError(
                "El índice está vacío. Ejecutá primero: python -m rag.ingest"
            )

        result: dict[str, Any] = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        return [
            RetrievedProduct(text=text, metadata=metadata, distance=distance)
            for text, metadata, distance in zip(
                documents, metadatas, distances, strict=True
            )
        ]
