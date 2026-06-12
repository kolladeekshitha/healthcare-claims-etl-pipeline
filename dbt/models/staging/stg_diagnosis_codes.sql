select
    cast(diagnosis_code as varchar) as diagnosis_code,
    trim(diagnosis_description) as diagnosis_description,
    trim(diagnosis_category) as diagnosis_category
from {{ source('raw_claims', 'diagnosis_codes') }}
