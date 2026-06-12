with source as (
    select * from {{ source('raw_claims', 'claims') }}
),

renamed as (
    select
        cast(claim_id as varchar) as claim_id,
        cast(patient_id as varchar) as patient_id,
        cast(provider_id as varchar) as provider_id,
        cast(diagnosis_code as varchar) as diagnosis_code,
        cast(claim_amount as numeric(12, 2)) as claim_amount,
        cast(claim_date as date) as claim_date,
        lower(trim(claim_status)) as claim_status,
        trim(insurance_plan) as insurance_plan,
        upper(trim(state)) as claim_state
    from source
)

select * from renamed
