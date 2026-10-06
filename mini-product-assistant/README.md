# Mini Product Assistant — Demo V1 RAG

Proyecto educativo de **Sistemas de Soporte de Decisión**. La V1 extiende la extracción
estructurada de la V0 con una base local de productos, búsqueda semántica y una respuesta
fundamentada únicamente en los datos recuperados.

## Evolución de la demo

V0:

```text
Natural language → Structured Output
```

V1:

```text
Natural language
→ ProductRequirements
→ Semantic Retrieval
→ Context
→ LLM
→ Grounded Answer
```

El workflow es fijo y está controlado por Python. El retriever **no es una Tool**: el LLM
no decide si buscar ni cuál es el paso siguiente. No hay agentes, routing, planificación,
function calling ni búsquedas externas.

## Componentes

- `data/products.xlsx`: fuente de conocimiento sintética (hoja `Products`).
- `rag/loader.py`: carga el Excel, valida columnas y normaliza vacíos a `None`.
- `rag/document_builder.py`: convierte una fila estructurada en texto más metadata.
- `rag/embeddings.py`: genera embeddings con Ollama.
- `rag/vector_store.py`: persiste y consulta vectores en Chroma local.
- `rag/ingest.py`: proceso independiente de indexación.
- `rag/retriever.py`: semantic search y construcción del contexto.
- `llm.py`: conserva Structured Outputs de V0 y agrega generación grounded.
- `app.py`: ejecuta y muestra las etapas del pipeline en orden.

## Conceptos clave

Un **embedding** es una representación numérica de un texto. Textos semánticamente
parecidos tienden a quedar cerca en el espacio vectorial, lo que permite recuperar
productos relevantes aunque la consulta no use exactamente las palabras del Excel.

Cada fila se convierte en texto porque el modelo de embeddings recibe lenguaje, no una
fila tabular. Las columnas originales útiles también se guardan como metadata. En este
dataset, **una fila = un producto = un documento/chunk**: cada producto ya es una unidad
semántica completa. El chunking depende de la estructura del conocimiento; un documento
largo podría dividirse por secciones, pero aquí hacerlo por caracteres mezclaría o
fragmentaría innecesariamente una ficha.

Chroma guarda el texto, la metadata y el embedding de cada producto. La búsqueda usa
distancia coseno: cuanto menor es la distancia mostrada, mayor es la similitud. Una
**grounded answer** es una respuesta cuyas afirmaciones se apoyan exclusivamente en el
contexto recuperado. Si el Excel no contiene garantía, stock, disponibilidad, promociones
o fecha de entrega, la aplicación debe reconocer que no tiene esa información.

Esta demo enfatiza semantic retrieval. Para restricciones exactas como `price <= 500`,
un sistema productivo podría combinar búsqueda semántica con filtros estructurados; esa
optimización queda fuera del alcance de V1.

## Requisitos y configuración

- Python 3.11 o superior.
- [Ollama](https://ollama.com/) instalado y ejecutándose.
- Un modelo de chat y uno de embeddings disponibles localmente.

```bash
python -m venv .venv
pip install -r requirements.txt
ollama pull llama3.1
ollama pull nomic-embed-text
```

En Windows PowerShell activá el entorno con `.venv\Scripts\Activate.ps1`; en macOS o
Linux, con `source .venv/bin/activate`.

La configuración es opcional y puede definirse copiando `.env.example` a `.env`:

```env
OLLAMA_MODEL=llama3.1:latest
OLLAMA_HOST=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
DEBUG_RAG=false
```

`DEBUG_RAG=true` muestra metadata y el contexto completo enviado al LLM.

## Indexación, ejecución y tests

La ingesta se ejecuta una vez (y nuevamente cuando cambie el Excel):

```bash
python -m rag.ingest
```

Luego iniciá la CLI. Las consultas reutilizan el índice persistido y no vuelven a generar
los embeddings de todos los productos:

```bash
python app.py
```

Ejecutá las pruebas determinísticas, que no llaman realmente al LLM ni al modelo de
embeddings:

```bash
pytest
```

## Consultas sugeridas

```text
Busco un monitor de 27 pulgadas para programar, hasta USD 500 y con USB-C.
Quiero un monitor de 27 pulgadas para gaming, de alta tasa de refresco y menos de USD 400.
Necesito un monitor para diseño y edición de contenido, idealmente de 27 pulgadas y USB-C.
Busco una notebook para programar y estudiar, con 16 GB de RAM o más y portátil.
Busco auriculares inalámbricos para trabajar y hacer videollamadas.
¿Cuál tiene mejor garantía?
```

La última consulta debe indicar que la base no contiene información suficiente para
comparar garantías, en vez de inventar una respuesta.
