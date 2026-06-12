# Healthcare Claims ETL Architecture

This project simulates a payer claims analytics platform with clear separation between ingestion, validation, scalable processing, warehouse modeling, and analytics consumption.

```mermaid
flowchart TD
    A["Source CSV extracts"] --> B["Python ingestion"]
    B --> C["Schema validation"]
    B --> D["Ingestion audit records"]
    C --> E["Staged CSVs"]
    E --> F["PySpark transformations"]
    F --> G["Silver claims_enriched"]
    G --> H["Gold parquet summaries"]
    E --> I["Snowflake RAW schema"]
    I --> J["dbt staging models"]
    J --> K["dbt intermediate claims_enriched"]
    K --> L["dbt analytics marts"]
    L --> M["Dashboard-ready KPIs"]
    N["Airflow DAG"] -.orchestrates.-> B
    N -.orchestrates.-> F
    N -.orchestrates.-> O["Data quality checks"]
    N -.orchestrates.-> L
```

## Design Principles

- Keep raw source structures available for replay and reconciliation.
- Validate required columns, key uniqueness, accepted status values, and reference integrity before publishing analytics.
- Use Spark for distributed joins and aggregates when claim volume grows beyond single-machine processing.
- Use dbt to make warehouse transformations testable, documented, and lineage-aware.
- Publish gold tables at grains that directly map to BI questions.

## Operational Flow

1. Airflow starts `ingest_raw_data`.
2. Python reads source CSVs, validates schemas, standardizes values, removes duplicate keys, and writes ingestion audit records.
3. PySpark reads staged files and creates silver enriched claims plus gold parquet summaries.
4. Data quality checks validate claim identifiers, amounts, statuses, and foreign keys.
5. dbt builds and tests Snowflake staging, intermediate, and analytics models.
6. The final publish task marks gold tables as ready for BI consumption.
