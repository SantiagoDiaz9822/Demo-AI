"""Modelos de datos de la Demo V0."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# Representa los criterios de compra extraídos del mensaje del usuario.
class ProductRequirements(BaseModel):
    """Requisitos de compra extraídos del mensaje del usuario."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    category: str = Field(description="Categoría breve en inglés del producto pedido.")
    brand: str | None = Field(
        default=None,
        description="Marca mencionada explícitamente; null si no aparece en el mensaje.",
    )
    max_price: float | None = Field(
        default=None,
        gt=0,
        description="Precio máximo explícito; null si el mensaje no indica un presupuesto.",
    )
    size_inches: int | None = Field(
        default=None,
        gt=0,
        description="Pulgadas explícitas; null si el mensaje no indica un tamaño.",
    )
    use_case: str | None = Field(
        default=None,
        description="Finalidad expresada por el usuario; null si no explica para qué lo usará.",
    )

    # Normaliza la categoría a minúsculas y rechaza valores vacíos.
    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        normalized = value.casefold()
        if not normalized:
            raise ValueError("La categoría no puede estar vacía.")
        return normalized

    # Normaliza el caso de uso a minúsculas cuando fue informado.
    @field_validator("use_case")
    @classmethod
    def normalize_use_case(cls, value: str | None) -> str | None:
        return value.casefold() if value else None

    # Convierte strings opcionales vacíos en None después de validar el modelo.
    @model_validator(mode="after")
    def empty_optional_strings_become_none(self) -> Self:
        if not self.brand:
            self.brand = None
        if not self.use_case:
            self.use_case = None
        return self
