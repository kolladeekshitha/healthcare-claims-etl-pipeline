select
    claim_id,
    patient_id,
    provider_id,
    diagnosis_code,
    claim_amount,
    claim_date,
    claim_month,
    claim_status,
    insurance_plan,
    claim_state,
    provider_name,
    provider_type,
    diagnosis_category
from {{ ref('int_claims_enriched') }}
