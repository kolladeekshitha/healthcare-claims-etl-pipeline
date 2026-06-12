# Medallion Architecture

This project uses a Bronze, Silver, and Gold pattern to separate raw ingestion from cleaned data and business-ready analytics.

## Bronze

Bronze represents the source-aligned layer. In this project, Bronze includes the sample CSV extracts in `data/sample` and the Snowflake `RAW` schema.

Characteristics:

- Preserves the operational source structure.
- Keeps claim, patient, provider, and diagnosis data separate.
- Supports replay, reconciliation, and auditability.

## Silver

Silver represents conformed and validated data. In this project, Silver includes validated files in `data/staging`, enriched parquet output in `data/silver`, and dbt staging/intermediate models.

Transformations:

- Standardize dates, strings, status values, and numeric claim amounts.
- Remove duplicate claim identifiers.
- Validate required fields.
- Join claims to patient, provider, and diagnosis dimensions.
- Add reusable fields such as `claim_month`, `diagnosis_category`, and `network_status`.

## Gold

Gold represents business-facing marts. In this project, Gold includes parquet outputs in `data/gold` and dbt mart models in the Snowflake analytics schema.

Gold tables:

- `provider_claims_summary`
- `claim_kpi_summary`
- `network_claims_summary`
- `state_claims_summary`
- `diagnosis_claims_summary`
- `monthly_claims_summary`
- `fct_claims`

These tables are designed for dashboards, executive summaries, and payer analytics use cases.
