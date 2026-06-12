from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_SAMPLE_DIR = DATA_DIR / "sample"
STAGING_DIR = DATA_DIR / "staging"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
AUDIT_DIR = DATA_DIR / "audit"

ALLOWED_CLAIM_STATUSES = {"approved", "denied", "pending", "paid"}

PRIMARY_KEYS = {
    "claims": "claim_id",
    "patients": "patient_id",
    "providers": "provider_id",
    "diagnosis_codes": "diagnosis_code",
}

SCHEMAS = {
    "claims": {
        "claim_id": "string",
        "patient_id": "string",
        "provider_id": "string",
        "diagnosis_code": "string",
        "claim_amount": "float",
        "claim_date": "date",
        "claim_status": "string",
        "insurance_plan": "string",
        "state": "string",
    },
    "patients": {
        "patient_id": "string",
        "first_name": "string",
        "last_name": "string",
        "date_of_birth": "date",
        "gender": "string",
        "state": "string",
        "insurance_plan": "string",
    },
    "providers": {
        "provider_id": "string",
        "provider_name": "string",
        "provider_type": "string",
        "npi": "string",
        "state": "string",
        "network_status": "string",
    },
    "diagnosis_codes": {
        "diagnosis_code": "string",
        "diagnosis_description": "string",
        "diagnosis_category": "string",
    },
}
