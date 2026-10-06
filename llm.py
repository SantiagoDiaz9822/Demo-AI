"""Acceso a Ollama, encapsulado para el resto de la aplicación."""

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError
from pydantic import ValidationError

from models import ProductRequirements
from prompts import (
    EXTRACTION_INSTRUCTIONS,
    GROUNDED_ANSWER_INSTRUCTIONS,
    build_grounded_prompt,
)

DEFAULT_MODEL = "llama3.1:latest"
DEFAULT_HOST = "http://localhost:11434"


# Error base para fallos relacionados con el modelo de lenguaje.
class LLMError(RuntimeError):
    """Error comprensible para la capa de presentación."""


# Indica que el host o el modelo configurado no están disponibles.
class LLMConfigurationError(LLMError):
    """La configuración necesaria para llamar al modelo es inválida."""


# Indica que el modelo devolvió una respuesta vacía o inválida.
class LLMResponseError(LLMError):
    """El proveedor no devolvió un resultado estructurado válido."""


# Extrae requisitos estructurados y validados desde la consulta del usuario.
def extract_product_requirements(user_input: str) -> ProductRequirements:
    """Convierte una descripción libre en requisitos de producto validados."""

    cleaned_input = user_input.strip()
    if not cleaned_input:
        raise ValueError("La descripción del producto no puede estar vacía.")

    load_dotenv()
    model = os.getenv("OLLAMA_MODEL") or DEFAULT_MODEL
    host = os.getenv("OLLAMA_HOST") or DEFAULT_HOST
    client = Client(host=host)

    try:
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": EXTRACTION_INSTRUCTIONS},
                {"role": "user", "content": cleaned_input},
            ],
            format=ProductRequirements.model_json_schema(),
            options={"temperature": 0},
        )
    except ConnectionError as error:
        raise LLMError(
            "No se pudo conectar con Ollama. Verificá que esté instalado y ejecutándose."
        ) from error
    except ResponseError as error:
        if error.status_code == 404:
            raise LLMConfigurationError(
                f"No se encontró el modelo '{model}'. Instalalo con: ollama pull {model}"
            ) from error
        raise LLMError("Ollama no pudo procesar la solicitud.") from error
    except ValidationError as error:
        raise LLMResponseError(
            "El modelo devolvió una respuesta que no cumple el esquema esperado."
        ) from error

    if not response.message.content:
        raise LLMResponseError(
            "El modelo no devolvió requisitos estructurados. Intentá reformular la consulta."
        )

    try:
        return ProductRequirements.model_validate_json(response.message.content)
    except ValidationError as error:
        raise LLMResponseError(
            "El modelo devolvió una respuesta que no cumple el esquema esperado."
        ) from error


# Genera una respuesta basada exclusivamente en el contexto recuperado.
def generate_grounded_answer(user_input: str, context: str) -> str:
    """Genera una respuesta limitada a la evidencia recuperada."""

    cleaned_input = user_input.strip()
    if not cleaned_input:
        raise ValueError("La pregunta no puede estar vacÃ­a.")
    if not context.strip():
        return "No tengo informaciÃ³n suficiente en la base de conocimiento para responder."

    load_dotenv()
    model = os.getenv("OLLAMA_MODEL") or DEFAULT_MODEL
    host = os.getenv("OLLAMA_HOST") or DEFAULT_HOST
    client = Client(host=host)

    try:
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": GROUNDED_ANSWER_INSTRUCTIONS},
                {
                    "role": "user",
                    "content": build_grounded_prompt(cleaned_input, context),
                },
            ],
            options={"temperature": 0},
        )
    except ConnectionError as error:
        raise LLMError(
            "No se pudo conectar con Ollama. VerificÃ¡ que estÃ© instalado y ejecutÃ¡ndose."
        ) from error
    except ResponseError as error:
        if error.status_code == 404:
            raise LLMConfigurationError(
                f"No se encontrÃ³ el modelo '{model}'. Instalalo con: ollama pull {model}"
            ) from error
        raise LLMError("Ollama no pudo generar la respuesta.") from error

    answer = response.message.content.strip() if response.message.content else ""
    if not answer:
        raise LLMResponseError("El modelo no devolviÃ³ una respuesta.")
    return answer
