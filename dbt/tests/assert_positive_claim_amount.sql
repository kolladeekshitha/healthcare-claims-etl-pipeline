select claim_id, claim_amount
from {{ ref('stg_claims') }}
where claim_amount <= 0
