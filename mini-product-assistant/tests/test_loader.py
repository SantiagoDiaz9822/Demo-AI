from pathlib import Path

from openpyxl import Workbook

from rag.loader import load_products

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "products.xlsx"


def test_loads_all_products_from_products_sheet() -> None:
    products = load_products(DATA_PATH)

    assert len(products) == 20
    assert products[0].product_id == "monitor_samsung_viewfinity_s7_demo"
    assert products[0].category == "monitor"
    assert products[0].price_usd == 429


def test_normalizes_empty_cells_to_none(tmp_path: Path) -> None:
    source = tmp_path / "products.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Products"
    sheet.append(["product_id", "category", "product_name", "brand"])
    sheet.append(["product_1", "monitor", "Demo", "   "])
    workbook.save(source)

    products = load_products(source)

    assert products[0].brand is None
