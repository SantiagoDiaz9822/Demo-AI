# Mini Product Assistant — Demo V0

Proyecto educativo para la materia **Sistemas de Soporte de Decisión**. Esta primera
versión muestra cómo un LLM puede transformar una necesidad escrita en lenguaje natural
en datos estructurados y validados que una aplicación puede utilizar.

```text
mensaje del usuario → prompt + esquema → LLM → ProductRequirements → JSON
```

## Objetivo

La aplicación pide una descripción de compra, usa Structured Outputs de Ollama para
extraer los requisitos y valida el resultado directamente con un modelo Pydantic. Todo
se ejecuta localmente: no requiere una API key ni envía la consulta a una API externa.

El esquema contiene:

- categoría;
- marca;
- precio máximo;
- tamaño en pulgadas;
- caso de uso.

Los valores que el usuario no proporciona se representan como `null` en JSON.

## Requisitos

- Python 3.11 o superior;
- [Ollama](https://ollama.com/) instalado y ejecutándose;
- el modelo local `llama3.1:latest` (o uno alternativo configurable).

## Setup

Creá un entorno virtual:

```bash
python -m venv .venv
```

Activación en Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activación en macOS o Linux:

```bash
source .venv/bin/activate
```

Instalá las dependencias:

```bash
pip install -r requirements.txt
```

Descargá el modelo predeterminado si todavía no lo tenés:

```bash
ollama pull llama3.1
```

La configuración funciona sin un archivo `.env`. Para usar otro modelo o servidor,
copiá `.env.example` como `.env` y ajustá sus valores.

## Ejecución

```bash
python app.py
```

Ejemplo de consulta:

```text
Quiero un monitor Samsung de menos de 500 dólares y de 27 pulgadas.
```

La aplicación presenta primero una vista legible y después el JSON validado.

## Tests

Las pruebas unitarias no llaman al modelo ni requieren una API key:

```bash
pytest
```

## Alcance actual

Esta versión **no busca productos ni realiza recomendaciones reales**. Tampoco incluye
RAG, embeddings, una base de productos, tools, agentes, memoria, voz, API web ni
frontend. La demo termina al obtener un `ProductRequirements` y su JSON.

## Evolución futura

- V1 → retrieval / RAG
- V2 → tools
- V3 → agent / harness

Estas etapas se mencionan solamente como continuidad pedagógica y no están implementadas
en esta rama.
