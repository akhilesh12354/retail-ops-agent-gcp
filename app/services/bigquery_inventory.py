"""BigQuery inventory repository.

Imports are lazy so local tests can run without installing GCP dependencies.
"""

from __future__ import annotations


class BigQueryInventoryRepository:
    def __init__(self, project_id: str, dataset: str):
        self.project_id = project_id
        self.dataset = dataset

    def inventory_for(self, store_id: str, sku: str) -> dict:
        rows = self._query(
            """
            SELECT *
            FROM `{project}.{dataset}.inventory`
            WHERE store_id = @store_id AND sku = @sku
            LIMIT 1
            """,
            {"store_id": store_id, "sku": sku},
        )
        if not rows:
            raise KeyError(f"No inventory for store={store_id} sku={sku}")
        return rows[0]

    def inventory_by_sku(self, sku: str) -> list[dict]:
        return self._query(
            """
            SELECT *
            FROM `{project}.{dataset}.inventory`
            WHERE sku = @sku
            """,
            {"sku": sku},
        )

    def orders_for(self, store_id: str, sku: str) -> list[dict]:
        return self._query(
            """
            SELECT *
            FROM `{project}.{dataset}.orders`
            WHERE store_id = @store_id AND sku = @sku
            """,
            {"store_id": store_id, "sku": sku},
        )

    def capacity_rows(self) -> list[dict]:
        return self._query(
            """
            SELECT *
            FROM `{project}.{dataset}.store_capacity`
            """,
            {},
        )

    def _query(self, sql_template: str, params: dict[str, str]) -> list[dict]:
        from google.cloud import bigquery

        client = bigquery.Client(project=self.project_id)
        query = sql_template.format(project=self.project_id, dataset=self.dataset)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(key, "STRING", value)
                for key, value in params.items()
            ]
        )
        rows = client.query(query, job_config=job_config).result()
        return [dict(row) for row in rows]
