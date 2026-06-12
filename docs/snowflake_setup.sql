create database if not exists healthcare_claims;
create schema if not exists healthcare_claims.raw;
create schema if not exists healthcare_claims.staging;
create schema if not exists healthcare_claims.intermediate;
create schema if not exists healthcare_claims.analytics;

create or replace table healthcare_claims.raw.claims (
    claim_id varchar,
    patient_id varchar,
    provider_id varchar,
    diagnosis_code varchar,
    claim_amount number(12, 2),
    claim_date date,
    claim_status varchar,
    insurance_plan varchar,
    state varchar
);

create or replace table healthcare_claims.raw.patients (
    patient_id varchar,
    first_name varchar,
    last_name varchar,
    date_of_birth date,
    gender varchar,
    state varchar,
    insurance_plan varchar
);

create or replace table healthcare_claims.raw.providers (
    provider_id varchar,
    provider_name varchar,
    provider_type varchar,
    npi varchar,
    state varchar,
    network_status varchar
);

create or replace table healthcare_claims.raw.diagnosis_codes (
    diagnosis_code varchar,
    diagnosis_description varchar,
    diagnosis_category varchar
);

-- Example load pattern after uploading files to an internal or external Snowflake stage:
-- copy into healthcare_claims.raw.claims
-- from @healthcare_claims.raw.claims_stage/claims.csv
-- file_format = (type = csv skip_header = 1 field_optionally_enclosed_by = '"');
