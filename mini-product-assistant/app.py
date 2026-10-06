"""Interfaz de terminal de Mini Product Assistant — Demo V1 RAG."""

import json
import os

from dotenv import load_dotenv

from llm import LLMError, extract_product_requirements, generate_grounded_answer
from models import ProductRequirements, RetrievedProduct
from rag.embeddings import EmbeddingError
from rag.retriever import build_context, retrieve_relevant_products
from rag.vector_store import VectorStoreError


# Convierte los requisitos estructurados en texto legible para la terminal.
def format_requirements(requirements: ProductRequirements) -> str:
    """Prepara una vista legible del objeto estructurado."""

    price = (
        f"{requirements.max_price:g}"
        if requirements.max_price is not None
        else "no especificado"
    )
    size = (
        f'{requirements.size_inches}"'
        if requirements.size_inches is not None
        else "no especificado"
    )
    return "\n".join(
        [
            f"Categoría: {requirements.category}",
            f"Marca: {requirements.brand or 'no especificada'}",
            f"Precio máximo: {price}",
            f"Tamaño: {size}",
            f"Caso de uso: {requirements.use_case or 'no especificado'}",
        ]
    )


# Formatea los productos recuperados y sus distancias para mostrarlos en la CLI.
def format_retrieved_products(products: list[RetrievedProduct]) -> str:
    """Hace observable el retrieval antes de la generación final."""

    lines: list[str] = []
    for index, product in enumerate(products, start=1):
        metadata = product.metadata
        price = metadata.get("price_usd")
        price_text = f"USD {price:g}" if isinstance(price, (int, float)) else "-"
        lines.extend(
            [
                f"{index}. {metadata.get('product_name', '-')}",
                f"   categoría: {metadata.get('category', '-')}",
                f"   precio: {price_text}",
                f"   distancia coseno: {product.distance:.4f} (menor = más similar)",
            ]
        )
    return "\n".join(lines)


# Interpreta si la respuesta del usuario significa que desea otra consulta.
def wants_another_query(answer: str) -> bool:
    """Interpreta las respuestas afirmativas más comunes."""

    return answer.strip().casefold() in {"s", "sí", "si", "y", "yes"}


# Lee DEBUG_RAG y determina si debe mostrarse información interna del pipeline.
def _debug_enabled() -> bool:
    load_dotenv()
    return os.getenv("DEBUG_RAG", "false").strip().casefold() in {"1", "true", "yes"}


# Ejecuta el ciclo interactivo y coordina todas las etapas del pipeline RAG.
def main() -> None:
    print("Mini Product Assistant — Demo V1 RAG")

    while True:
        try:
            user_input = input("\n¿Qué producto estás buscando?\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return

        if not user_input.strip():
            print("La descripción no puede estar vacía.")
            continue

        try:
            print("\n--------------------------------")
            print("1. Requisitos detectados")
            print("--------------------------------")
            requirements = extract_product_requirements(user_input)
            print(format_requirements(requirements))

            print("\n--------------------------------")
            print("2. Retrieval")
            print("--------------------------------")
            products = retrieve_relevant_products(user_input, top_k=4)
            print(format_retrieved_products(products))

            context = build_context(products)
            if _debug_enabled():
                print("\n[DEBUG] Metadata recuperada:")
                for product in products:
                    print(json.dumps(product.metadata, ensure_ascii=False, indent=2))
                print("\n[DEBUG] Contexto enviado al LLM:")
                print(context)

            # El retrieval se ejecuta siempre desde la aplicación antes de generar.
            answer = generate_grounded_answer(user_input, context)
            print("\n--------------------------------")
            print("3. Respuesta grounded")
            print("--------------------------------")
            print(answer)
        except (LLMError, EmbeddingError, VectorStoreError, ValueError) as error:
            print(f"\nError: {error}")

        try:
            repeat = input("\n¿Querés hacer otra consulta? [s/N]\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return
        if not wants_another_query(repeat):
            print("Hasta luego.")
            return


if __name__ == "__main__":
    main()
