"""CSV ingestion and schema validation for raw healthcare claims data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from config import AUDIT_DIR, PRIMARY_KEYS, RAW_SAMPLE_DIR, SCHEMAS, STAGING_DIR


class DataValidationError(ValueError):
    """Raised when an input file does not satisfy expected quality rules."""


def _parse_dates(df: pd.DataFrame, schema: dict[str, str]) -> pd.DataFrame:
    for column, dtype in schema.items():
        if dtype == "date":
            df[column] = pd.to_datetime(df[column], errors="coerce").dt.date
    return df


def validate_schema(df: pd.DataFrame, dataset_name: str) -> None:
    expected_columns = list(SCHEMAS[dataset_name].keys())
    missing = sorted(set(expected_columns) - set(df.columns))
    extra = sorted(set(df.columns) - set(expected_columns))

    if missing:
        raise DataValidationError(f"{dataset_name} is missing columns: {missing}")
    if extra:
        raise DataValidationError(f"{dataset_name} has unexpected columns: {extra}")


def clean_dataframe(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    schema = SCHEMAS[dataset_name]
    df = df.copy()

    validate_schema(df, dataset_name)

    for column, dtype in schema.items():
        if dtype == "string":
            df[column] = df[column].astype("string").str.strip()
        elif dtype == "float":
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = _parse_dates(df, schema)
    df = df.drop_duplicates()

    primary_key = PRIMARY_KEYS[dataset_name]
    df = df.drop_duplicates(subset=[primary_key], keep="first")

    required_columns = [primary_key]
    if dataset_name == "claims":
        required_columns.extend(["patient_id", "provider_id", "diagnosis_code", "claim_amount", "claim_date"])

    return df.dropna(subset=required_columns)


def write_audit_record(dataset_name: str, source_rows: int, staged_rows: int, audit_dir: Path = AUDIT_DIR) -> Path:
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / f"{dataset_name}_ingestion_audit.json"
    audit_record = {
        "dataset": dataset_name,
        "source_rows": source_rows,
        "staged_rows": staged_rows,
        "rejected_or_deduplicated_rows": source_rows - staged_rows,
        "primary_key": PRIMARY_KEYS[dataset_name],
    }
    audit_path.write_text(json.dumps(audit_record, indent=2), encoding="utf-8")
    return audit_path


def ingest_dataset(dataset_name: str, source_dir: Path = RAW_SAMPLE_DIR, target_dir: Path = STAGING_DIR) -> Path:
    source_path = source_dir / f"{dataset_name}.csv"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{dataset_name}.csv"

    df = pd.read_csv(source_path, dtype="string")
    cleaned = clean_dataframe(df, dataset_name)
    cleaned.to_csv(target_path, index=False)
    write_audit_record(dataset_name, len(df), len(cleaned))
    return target_path


def ingest_all(source_dir: Path = RAW_SAMPLE_DIR, target_dir: Path = STAGING_DIR) -> list[Path]:
    return [ingest_dataset(dataset_name, source_dir, target_dir) for dataset_name in SCHEMAS]


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest sample healthcare CSV files to staging.")
    parser.add_argument("--source-dir", type=Path, default=RAW_SAMPLE_DIR)
    parser.add_argument("--target-dir", type=Path, default=STAGING_DIR)
    args = parser.parse_args()

    written_files = ingest_all(args.source_dir, args.target_dir)
    for file_path in written_files:
        print(f"Wrote {file_path}")


if __name__ == "__main__":
    main()
