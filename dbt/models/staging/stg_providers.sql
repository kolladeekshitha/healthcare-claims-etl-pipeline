select
    cast(provider_id as varchar) as provider_id,
    trim(provider_name) as provider_name,
    trim(provider_type) as provider_type,
    cast(npi as varchar) as npi,
    upper(trim(state)) as provider_state,
    lower(trim(network_status)) as network_status
from {{ source('raw_claims', 'providers') }}
