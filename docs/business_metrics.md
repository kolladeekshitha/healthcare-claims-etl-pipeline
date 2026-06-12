# Business Metrics

The analytics layer focuses on payer claims operations, provider cost monitoring, and clinical spend analysis.

| Metric | Calculation | Grain | Primary Consumers |
| --- | --- | --- | --- |
| Claim Volume | Count distinct `claim_id` | Provider, state, diagnosis, month | Operations, Finance |
| Total Claim Amount | Sum `claim_amount` | Provider, state, diagnosis, month | Finance |
| Average Claim Amount | Sum `claim_amount` / count distinct `claim_id` | Provider, diagnosis | Provider Operations |
| Denial Rate | Denied claims / total claims | Provider, state, month | Claims Operations |
| Pending Exposure | Sum `claim_amount` where status is pending | State, month | Finance |
| Paid Amount | Sum `claim_amount` where status is paid | Provider, month | Finance |
| Approved Amount | Sum `claim_amount` where status is approved | Provider, diagnosis | Finance |
| Out-of-Network Spend | Sum approved or paid amount where network_status is out_of_network | Provider, state | Network Management |
| Diagnosis Category Spend | Sum claim amount by diagnosis_category | Diagnosis category, month | Clinical Analytics |

## Gold Tables Supporting Metrics

| Gold Table | Metrics |
| --- | --- |
| `claim_kpi_summary` | Claim volume, submitted amount, approved/paid amount, pending exposure, denial rate, out-of-network spend |
| `provider_claims_summary` | Provider claim volume, total amount, average amount |
| `network_claims_summary` | In-network and out-of-network approved/paid spend |
| `diagnosis_claims_summary` | Diagnosis-level volume and spend |
| `state_claims_summary` | State-level volume and spend |
| `monthly_claims_summary` | Monthly claim volume and spend trend |

## Example Dashboard Questions

- Which providers are driving the highest paid and approved claim spend?
- Are denied claims concentrated in specific states or providers?
- Which diagnosis categories contribute the most to total cost?
- How is monthly claim volume trending?
- How much pending claim exposure remains unresolved?
- What share of reimbursable spend is out of network?
