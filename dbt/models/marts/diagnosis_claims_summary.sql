select
    diagnosis_code,
    diagnosis_category,
    count(distinct claim_id) as claim_count,
    sum(claim_amount) as total_claim_amount
from {{ ref('fct_claims') }}
where claim_status in ('approved', 'paid')
group by 1, 2
