from app import format_requirements, wants_another_query
from models import ProductRequirements


def test_formats_missing_values_for_people() -> None:
    requirements = ProductRequirements(category="laptop", use_case="study")

    assert format_requirements(requirements) == "\n".join(
        [
            "Categoría: laptop",
            "Marca: no especificada",
            "Precio máximo: no especificado",
            "Tamaño: no especificado",
            "Caso de uso: study",
        ]
    )


def test_accepts_spanish_yes_answer() -> None:
    assert wants_another_query(" Sí ") is True
    assert wants_another_query("n") is False
