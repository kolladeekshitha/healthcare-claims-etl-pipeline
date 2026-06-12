select
    provider_id,
    provider_name,
    provider_type,
    count(distinct claim_id) as claim_count,
    sum(claim_amount) as total_claim_amount,
    avg(claim_amount) as avg_claim_amount
from {{ ref('fct_claims') }}
where claim_status in ('approved', 'paid')
group by 1, 2, 3
