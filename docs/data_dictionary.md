# Data Dictionary

## claims.csv

| Column | Description |
| --- | --- |
| claim_id | Unique claim transaction identifier. |
| patient_id | Foreign key to the patient reference table. |
| provider_id | Foreign key to the provider reference table. |
| diagnosis_code | ICD diagnosis code for the claim. |
| claim_amount | Billed or adjudicated claim amount. |
| claim_date | Date the claim was submitted or processed. |
| claim_status | Claim lifecycle status: approved, denied, pending, or paid. |
| insurance_plan | Member insurance plan attached to the claim. |
| state | State where the claim was filed. |

## patients.csv

| Column | Description |
| --- | --- |
| patient_id | Unique patient identifier. |
| first_name | Patient first name for sample data only. |
| last_name | Patient last name for sample data only. |
| date_of_birth | Patient birth date. |
| gender | Patient gender marker in source data. |
| state | Patient residence state. |
| insurance_plan | Current insurance plan. |

## providers.csv

| Column | Description |
| --- | --- |
| provider_id | Unique provider identifier. |
| provider_name | Provider organization name. |
| provider_type | Provider classification, such as primary care or specialist. |
| npi | National Provider Identifier. |
| state | Provider operating state. |
| network_status | In-network or out-of-network status. |

## diagnosis_codes.csv

| Column | Description |
| --- | --- |
| diagnosis_code | ICD diagnosis code. |
| diagnosis_description | Human-readable diagnosis description. |
| diagnosis_category | Reporting category for diagnosis analytics. |

## ingestion audit records

| Field | Description |
| --- | --- |
| dataset | Dataset name processed by the ingestion job. |
| source_rows | Number of rows read from the source file. |
| staged_rows | Number of rows written after validation and deduplication. |
| rejected_or_deduplicated_rows | Difference between source and staged rows. |
| primary_key | Primary key used for duplicate handling. |
