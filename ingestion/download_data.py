"""Download the Olist Brazilian E-Commerce dataset into a local directory."""
from pathlib import Path
import shutil

import kagglehub

DATASET = "olistbr/brazilian-ecommerce"

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def download_dataset(dest_dir: Path) -> list[Path]:
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    cache_path = Path(kagglehub.dataset_download(DATASET))

    copied = []
    for filename in EXPECTED_FILES:
        src = cache_path / filename
        dst = dest_dir / filename
        shutil.copyfile(src, dst)
        copied.append(dst)
    return copied


if __name__ == "__main__":
    files = download_dataset(Path("data/raw"))
    print(f"Downloaded {len(files)} files to data/raw/")
