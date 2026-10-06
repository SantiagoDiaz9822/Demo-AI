"""Interfaz de terminal de Mini Product Assistant — Demo V0."""

from llm import LLMError, extract_product_requirements
from models import ProductRequirements


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


# Interpreta si la respuesta del usuario significa que desea otra consulta.
def wants_another_query(answer: str) -> bool:
    """Interpreta las respuestas afirmativas más comunes."""

    return answer.strip().casefold() in {"s", "sí", "si", "y", "yes"}


# Ejecuta el ciclo interactivo de extracción estructurada de requisitos.
def main() -> None:
    print("Mini Product Assistant — Demo V0")

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
            print("extrayendo requisitos...")
            requirements = extract_product_requirements(user_input)
        except (LLMError, ValueError) as error:
            print(f"\nError: {error}")
        else:
            print("\nRequisitos detectados:\n")
            print(format_requirements(requirements))
            print("\nJSON:\n")
            print(requirements.model_dump_json(indent=2))

        try:
            answer = input("\n¿Querés hacer otra consulta? [s/N]\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return
        if not wants_another_query(answer):
            print("Hasta luego.")
            return


if __name__ == "__main__":
    main()
