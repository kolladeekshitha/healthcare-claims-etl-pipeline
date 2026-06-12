with claims as (
    select * from {{ ref('stg_claims') }}
),

patients as (
    select * from {{ ref('stg_patients') }}
),

providers as (
    select * from {{ ref('stg_providers') }}
),

diagnosis as (
    select * from {{ ref('stg_diagnosis_codes') }}
)

select
    claims.claim_id,
    claims.patient_id,
    patients.first_name || ' ' || patients.last_name as patient_name,
    patients.gender as patient_gender,
    claims.provider_id,
    providers.provider_name,
    providers.provider_type,
    providers.network_status,
    claims.diagnosis_code,
    diagnosis.diagnosis_description,
    diagnosis.diagnosis_category,
    claims.claim_amount,
    claims.claim_date,
    to_char(claims.claim_date, 'YYYY-MM') as claim_month,
    claims.claim_status,
    claims.insurance_plan,
    claims.claim_state
from claims
left join patients
    on claims.patient_id = patients.patient_id
left join providers
    on claims.provider_id = providers.provider_id
left join diagnosis
    on claims.diagnosis_code = diagnosis.diagnosis_code
