import duckdb

from ingestion.download_data import download_dataset, EXPECTED_FILES


def test_download_dataset_produces_expected_files(tmp_path):
    files = download_dataset(tmp_path)

    assert len(files) == len(EXPECTED_FILES)
    for filename in EXPECTED_FILES:
        assert (tmp_path / filename).exists()


def test_orders_file_has_expected_row_count(tmp_path):
    download_dataset(tmp_path)

    con = duckdb.connect()
    count = con.execute(
        f"select count(*) from read_csv_auto('{tmp_path}/olist_orders_dataset.csv')"
    ).fetchone()[0]

    assert count == 99441
