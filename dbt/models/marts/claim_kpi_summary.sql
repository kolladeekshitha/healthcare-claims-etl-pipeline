select
    count(distinct claim_id) as claim_count,
    sum(claim_amount) as total_submitted_amount,
    sum(case when claim_status in ('approved', 'paid') then claim_amount else 0 end) as approved_paid_amount,
    sum(case when claim_status = 'pending' then claim_amount else 0 end) as pending_exposure,
    round(
        count(distinct case when claim_status = 'denied' then claim_id end)
        / nullif(count(distinct claim_id), 0) * 100,
        2
    ) as denial_rate_pct,
    sum(
        case
            when network_status = 'out_of_network'
                and claim_status in ('approved', 'paid')
                then claim_amount
            else 0
        end
    ) as out_of_network_approved_paid_amount
from {{ ref('int_claims_enriched') }}
