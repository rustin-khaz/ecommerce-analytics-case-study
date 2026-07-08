import duckdb

from ingestion.download_data import download_dataset
from ingestion.load_raw import load_raw_tables

EXPECTED_ROW_COUNTS = {
    "orders": 99441,
    "customers": 99441,
    "order_items": 112650,
    "order_payments": 103886,
    "order_reviews": 99224,
    "products": 32951,
    "sellers": 3095,
    "geolocation": 1000163,
    "product_category_name_translation": 71,
}


def test_load_raw_tables_matches_expected_row_counts(tmp_path):
    csv_dir = tmp_path / "raw"
    db_path = tmp_path / "olist.duckdb"
    download_dataset(csv_dir)

    row_counts = load_raw_tables(csv_dir, db_path)

    assert row_counts == EXPECTED_ROW_COUNTS


def test_raw_schema_exists_in_duckdb_file(tmp_path):
    csv_dir = tmp_path / "raw"
    db_path = tmp_path / "olist.duckdb"
    download_dataset(csv_dir)
    load_raw_tables(csv_dir, db_path)

    con = duckdb.connect(str(db_path))
    tables = con.execute(
        "select table_name from information_schema.tables where table_schema = 'raw'"
    ).fetchall()
    con.close()

    table_names = {t[0] for t in tables}
    assert table_names == set(EXPECTED_ROW_COUNTS.keys())
