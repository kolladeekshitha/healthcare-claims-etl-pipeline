from pathlib import Path

import pandas as pd

from data_quality import run_claim_quality_checks


def test_quality_checks_pass_for_valid_claims(tmp_path: Path):
    pd.DataFrame(
        [
            {
                "claim_id": "C1",
                "patient_id": "P1",
                "provider_id": "PR1",
                "diagnosis_code": "I10",
                "claim_amount": 100.0,
                "claim_date": "2025-01-01",
                "claim_status": "paid",
                "insurance_plan": "Aetna HMO",
                "state": "TX",
            }
        ]
    ).to_csv(tmp_path / "claims.csv", index=False)

    pd.DataFrame([{"patient_id": "P1"}]).to_csv(tmp_path / "patients.csv", index=False)
    pd.DataFrame([{"provider_id": "PR1"}]).to_csv(tmp_path / "providers.csv", index=False)
    pd.DataFrame([{"diagnosis_code": "I10"}]).to_csv(tmp_path / "diagnosis_codes.csv", index=False)

    assert run_claim_quality_checks(tmp_path) == []


def test_quality_checks_return_actionable_failures(tmp_path: Path):
    pd.DataFrame(
        [
            {
                "claim_id": "C1",
                "patient_id": "P404",
                "provider_id": "PR404",
                "diagnosis_code": "I10",
                "claim_amount": -5.0,
                "claim_date": "2025-01-01",
                "claim_status": "reversed",
                "insurance_plan": "Aetna HMO",
                "state": "TX",
            },
            {
                "claim_id": "C1",
                "patient_id": "P404",
                "provider_id": "PR404",
                "diagnosis_code": "BAD",
                "claim_amount": 10.0,
                "claim_date": "2025-01-02",
                "claim_status": "paid",
                "insurance_plan": "Aetna HMO",
                "state": "TX",
            },
        ]
    ).to_csv(tmp_path / "claims.csv", index=False)

    pd.DataFrame([{"patient_id": "P1"}]).to_csv(tmp_path / "patients.csv", index=False)
    pd.DataFrame([{"provider_id": "PR1"}]).to_csv(tmp_path / "providers.csv", index=False)
    pd.DataFrame([{"diagnosis_code": "I10"}]).to_csv(tmp_path / "diagnosis_codes.csv", index=False)

    failures = run_claim_quality_checks(tmp_path)

    assert any("non-positive" in failure for failure in failures)
    assert any("invalid values" in failure for failure in failures)
    assert any("do not exist" in failure for failure in failures)
    assert any("provider_id" in failure for failure in failures)
    assert any("diagnosis_code" in failure for failure in failures)
    assert any("duplicate claim_id" in failure for failure in failures)
