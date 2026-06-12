"""Reusable data quality checks for staged healthcare claims data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import ALLOWED_CLAIM_STATUSES, STAGING_DIR


def run_claim_quality_checks(staging_dir: Path = STAGING_DIR) -> list[str]:
    claims = pd.read_csv(staging_dir / "claims.csv", dtype={"claim_id": "string"})
    patients = pd.read_csv(staging_dir / "patients.csv", dtype={"patient_id": "string"})
    providers = pd.read_csv(staging_dir / "providers.csv", dtype={"provider_id": "string"})
    diagnosis_codes = pd.read_csv(staging_dir / "diagnosis_codes.csv", dtype={"diagnosis_code": "string"})

    failures: list[str] = []

    if claims["claim_id"].isna().any():
        failures.append("claim_id contains null values")

    claim_amount = pd.to_numeric(claims["claim_amount"], errors="coerce")
    if claim_amount.isna().any():
        failures.append("claim_amount contains null or non-numeric values")

    if (claim_amount <= 0).any():
        failures.append("claim_amount contains non-positive values")

    invalid_statuses = sorted(set(claims["claim_status"].dropna()) - ALLOWED_CLAIM_STATUSES)
    if invalid_statuses:
        failures.append(f"claim_status contains invalid values: {invalid_statuses}")

    missing_patients = sorted(set(claims["patient_id"].dropna()) - set(patients["patient_id"].dropna()))
    if missing_patients:
        failures.append(f"patient_id values do not exist in patients: {missing_patients}")

    missing_providers = sorted(set(claims["provider_id"].dropna()) - set(providers["provider_id"].dropna()))
    if missing_providers:
        failures.append(f"provider_id values do not exist in providers: {missing_providers}")

    missing_diagnosis_codes = sorted(
        set(claims["diagnosis_code"].dropna()) - set(diagnosis_codes["diagnosis_code"].dropna())
    )
    if missing_diagnosis_codes:
        failures.append(f"diagnosis_code values do not exist in diagnosis_codes: {missing_diagnosis_codes}")

    duplicate_claims = claims.loc[claims["claim_id"].duplicated(), "claim_id"].tolist()
    if duplicate_claims:
        failures.append(f"duplicate claim_id values found: {duplicate_claims}")

    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Run data quality checks against staged claims files.")
    parser.add_argument("--staging-dir", type=Path, default=STAGING_DIR)
    args = parser.parse_args()

    failures = run_claim_quality_checks(args.staging_dir)
    if failures:
        for failure in failures:
            print(f"FAILED: {failure}")
        raise SystemExit(1)

    print("All data quality checks passed.")


if __name__ == "__main__":
    main()
