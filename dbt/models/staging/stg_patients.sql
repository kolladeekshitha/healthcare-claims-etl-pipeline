select
    cast(patient_id as varchar) as patient_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    cast(date_of_birth as date) as date_of_birth,
    upper(trim(gender)) as gender,
    upper(trim(state)) as patient_state,
    trim(insurance_plan) as insurance_plan
from {{ source('raw_claims', 'patients') }}
