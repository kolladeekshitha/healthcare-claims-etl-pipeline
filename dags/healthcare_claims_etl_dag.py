"""Airflow DAG for the healthcare claims ETL portfolio project."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

PROJECT_ROOT = Path("/opt/airflow/project")

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="healthcare_claims_etl_pipeline",
    description="Ingest, transform, test, and publish healthcare claims analytics.",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["healthcare", "claims", "etl", "spark", "dbt"],
) as dag:
    ingest_raw_data = BashOperator(
        task_id="ingest_raw_data",
        bash_command=f"cd {PROJECT_ROOT} && python src/ingest.py",
    )

    run_spark_transformations = BashOperator(
        task_id="run_spark_transformations",
        bash_command=f"cd {PROJECT_ROOT} && spark-submit src/spark_transform.py",
    )

    run_data_quality_checks = BashOperator(
        task_id="run_data_quality_checks",
        bash_command=f"cd {PROJECT_ROOT} && python src/data_quality.py && pytest tests -q",
    )

    trigger_dbt_models = BashOperator(
        task_id="trigger_dbt_models",
        bash_command=f"cd {PROJECT_ROOT}/dbt && dbt deps --profiles-dir . && dbt run --profiles-dir . && dbt test --profiles-dir .",
    )

    publish_gold_tables = EmptyOperator(task_id="publish_gold_tables")

    ingest_raw_data >> run_spark_transformations >> run_data_quality_checks >> trigger_dbt_models >> publish_gold_tables
