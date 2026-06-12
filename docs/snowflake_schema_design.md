# Snowflake Schema Design

The Snowflake design separates raw persistence, dbt transformations, and analytics consumption. This keeps source loading, modeling, and reporting responsibilities clear.

## Database

`HEALTHCARE_CLAIMS`

## Schemas

| Schema | Purpose | Example Objects |
| --- | --- | --- |
| `RAW` | Source-aligned tables loaded from CSV extracts | `claims`, `patients`, `providers`, `diagnosis_codes` |
| `STAGING` | dbt views that standardize types and names | `stg_claims`, `stg_patients` |
| `INTERMEDIATE` | dbt views for reusable business joins | `int_claims_enriched` |
| `ANALYTICS` | Business-facing facts and marts | `fct_claims`, `provider_claims_summary` |

## Raw Tables

### RAW.claims

Grain: one claim transaction per `claim_id`.

Key fields:

- `claim_id`
- `patient_id`
- `provider_id`
- `diagnosis_code`
- `claim_amount`
- `claim_date`
- `claim_status`
- `insurance_plan`
- `state`

### RAW.patients

Grain: one patient per `patient_id`.

Used to validate referential integrity and enrich claim-level records with demographic attributes.

### RAW.providers

Grain: one provider per `provider_id`.

Used to support provider performance, network status, and state-level analysis.

### RAW.diagnosis_codes

Grain: one diagnosis reference row per `diagnosis_code`.

Used to group claim spend into clinical categories.

## Analytics Tables

| Table | Grain | Use Case |
| --- | --- | --- |
| `fct_claims` | One row per claim | Flexible claim-level reporting and drill-through |
| `claim_kpi_summary` | One row for executive KPIs | KPI scorecards and executive dashboard |
| `provider_claims_summary` | One row per provider | Provider cost and utilization ranking |
| `network_claims_summary` | One row per network status | Network leakage analysis |
| `state_claims_summary` | One row per state | Regional spend and volume reporting |
| `diagnosis_claims_summary` | One row per diagnosis | Clinical cost-driver analysis |
| `monthly_claims_summary` | One row per claim month | Trend reporting |

## Loading Strategy

For a production implementation:

- Load raw files into a Snowflake stage.
- Use `COPY INTO` to populate `RAW` tables.
- Run dbt staging models as views for low-cost normalization.
- Materialize mart tables in `ANALYTICS` for dashboard performance.
- Apply dbt tests before exposing refreshed tables to BI users.

## Performance Considerations

For larger claim volumes:

- Cluster `fct_claims` by `claim_date`, `claim_state`, or `provider_id` depending on dashboard filters.
- Use incremental dbt models for high-volume claims.
- Track source file metadata such as load timestamp, file name, and batch id.
- Add reconciliation checks between source row counts and staged row counts.
