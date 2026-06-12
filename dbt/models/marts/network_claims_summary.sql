select
    network_status,
    count(distinct claim_id) as claim_count,
    sum(claim_amount) as total_claim_amount
from {{ ref('int_claims_enriched') }}
where claim_status in ('approved', 'paid')
group by 1
