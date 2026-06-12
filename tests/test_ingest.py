import pandas as pd
import pytest

from ingest import DataValidationError, clean_dataframe, validate_schema


def test_validate_schema_rejects_missing_required_columns():
    df = pd.DataFrame({"claim_id": ["C1"]})

    with pytest.raises(DataValidationError):
        validate_schema(df, "claims")


def test_clean_claims_removes_duplicate_claim_ids_and_null_required_values():
    df = pd.DataFrame(
        [
            {
                "claim_id": "C1",
                "patient_id": "P1",
                "provider_id": "PR1",
                "diagnosis_code": "I10",
                "claim_amount": "100.00",
                "claim_date": "2025-01-01",
                "claim_status": "paid",
                "insurance_plan": "Aetna HMO",
                "state": "TX",
            },
            {
                "claim_id": "C1",
                "patient_id": "P1",
                "provider_id": "PR1",
                "diagnosis_code": "I10",
                "claim_amount": "100.00",
                "claim_date": "2025-01-01",
                "claim_status": "paid",
                "insurance_plan": "Aetna HMO",
                "state": "TX",
            },
            {
                "claim_id": None,
                "patient_id": "P2",
                "provider_id": "PR2",
                "diagnosis_code": "E11.9",
                "claim_amount": "75.00",
                "claim_date": "2025-01-02",
                "claim_status": "approved",
                "insurance_plan": "BlueCross PPO",
                "state": "CA",
            },
        ]
    )

    cleaned = clean_dataframe(df, "claims")

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["claim_id"] == "C1"
