"""Seed BigQuery with the synthetic demo CSVs."""

from __future__ import annotations

import os
import logging
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TABLES = {
    "inventory": ROOT / "data" / "sample_inventory.csv",
    "orders": ROOT / "data" / "sample_orders.csv",
    "store_capacity": ROOT / "data" / "sample_store_capacity.csv",
}


SCHEMAS = {
    "inventory": [
        ("store_id", "STRING"),
        ("store_name", "STRING"),
        ("sku", "STRING"),
        ("on_hand", "INTEGER"),
        ("reserved", "INTEGER"),
        ("safety_stock", "INTEGER"),
        ("distance_to_zip_27701_miles", "INTEGER"),
        ("default_distance_miles", "INTEGER"),
    ],
    "orders": [
        ("order_id", "STRING"),
        ("store_id", "STRING"),
        ("sku", "STRING"),
        ("channel", "STRING"),
        ("status", "STRING"),
        ("created_at", "TIMESTAMP"),
    ],
    "store_capacity": [
        ("store_id", "STRING"),
        ("daily_capacity", "INTEGER"),
        ("open_orders", "INTEGER"),
        ("peak_season_mode", "BOOLEAN"),
    ],
}


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def main() -> int:
    try:
        from google.cloud import bigquery
    except ImportError:
        logging.error("Install GCP dependencies first: pip install '.[gcp]'")
        return 1

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    dataset_name = os.environ.get("BIGQUERY_DATASET", "retail_ops_demo")
    location = os.environ.get("BIGQUERY_LOCATION", "US")
    if not project_id:
        logging.error("Set GOOGLE_CLOUD_PROJECT before seeding BigQuery.")
        return 1

    client = bigquery.Client(project=project_id)
    dataset_id = f"{project_id}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = location
    
    logging.info(f"Ensuring dataset {dataset_id} exists...")
    client.create_dataset(dataset, exists_ok=True)

    for table_name, csv_path in TABLES.items():
        if not csv_path.exists():
            logging.warning(f"Skipping {table_name}: File {csv_path} not found.")
            continue
            
        table_id = f"{dataset_id}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,  # Using the explicit schemas we defined
            schema=[
                bigquery.SchemaField(column_name, column_type)
                for column_name, column_type in SCHEMAS[table_name]
            ],
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            allow_jagged_rows=True,
            ignore_unknown_values=True,
        )
        with csv_path.open("rb") as handle:
            job = client.load_table_from_file(handle, table_id, job_config=job_config)
        job.result()
        table = client.get_table(table_id)
        logging.info(f"Successfully loaded {table.num_rows} rows into {table_id}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
