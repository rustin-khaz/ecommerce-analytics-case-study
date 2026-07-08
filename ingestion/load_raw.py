"""Load raw Olist CSVs into a DuckDB `raw` schema."""
from pathlib import Path

import duckdb

TABLE_TO_FILE = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv",
}


def load_raw_tables(csv_dir: Path, db_path: Path) -> dict[str, int]:
    csv_dir = Path(csv_dir)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path))
    con.execute("create schema if not exists raw")

    row_counts = {}
    for table_name, filename in TABLE_TO_FILE.items():
        csv_path = csv_dir / filename
        con.execute(
            f"create or replace table raw.{table_name} as "
            f"select * from read_csv_auto('{csv_path}')"
        )
        row_counts[table_name] = con.execute(
            f"select count(*) from raw.{table_name}"
        ).fetchone()[0]

    con.close()
    return row_counts


if __name__ == "__main__":
    counts = load_raw_tables(Path("data/raw"), Path("warehouse/olist.duckdb"))
    for table, count in counts.items():
        print(f"raw.{table}: {count} rows")
