"""Conversión explícita de una fila estructurada a un documento semántico."""

from models import ProductRecord, RAGDocument


# Convierte valores estructurados a una representación clara para el documento.
def _display(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


# Convierte un producto en el texto y la metadata usados por el vector store.
def product_to_document(product: ProductRecord) -> RAGDocument:
    """Construye un documento; un producto es la unidad natural de chunking."""

    fields = [
        ("Product", product.product_name),
        ("Category", product.category),
        ("Brand", product.brand),
        ("Price", f"USD {_display(product.price_usd)}" if product.price_usd is not None else None),
        ("Size", f"{_display(product.size_inches)} inches" if product.size_inches is not None else None),
        ("Resolution", product.resolution),
        ("Refresh rate", f"{_display(product.refresh_rate_hz)} Hz" if product.refresh_rate_hz is not None else None),
        ("USB-C", product.usb_c),
        ("Power Delivery", f"{_display(product.power_delivery_w)}W" if product.power_delivery_w is not None else None),
        ("Connectivity", product.connectivity),
        ("Recommended use", product.recommended_use),
        ("Description", product.description),
        ("Features", product.features),
    ]
    text = "\n".join(
        f"{label}: {_display(value)}" for label, value in fields if value is not None
    )
    metadata = {
        key: value
        for key, value in product.model_dump().items()
        if value is not None and isinstance(value, (str, int, float, bool))
    }
    return RAGDocument(text=text, metadata=metadata)
