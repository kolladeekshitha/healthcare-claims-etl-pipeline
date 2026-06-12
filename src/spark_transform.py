"""PySpark transformations from staged CSVs to silver and gold analytics layers."""

from __future__ import annotations

import argparse
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, DoubleType

from config import GOLD_DIR, SILVER_DIR, STAGING_DIR


def create_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("healthcare-claims-etl-pipeline")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def read_csv(spark: SparkSession, path: Path) -> DataFrame:
    return spark.read.option("header", True).option("inferSchema", True).csv(str(path))


def build_silver_claims(
    claims: DataFrame,
    patients: DataFrame,
    providers: DataFrame,
    diagnosis_codes: DataFrame,
) -> DataFrame:
    cleaned_claims = (
        claims.withColumn("claim_amount", F.col("claim_amount").cast(DoubleType()))
        .withColumn("claim_date", F.col("claim_date").cast(DateType()))
        .withColumn("claim_status", F.lower(F.trim(F.col("claim_status"))))
        .withColumn("claim_month", F.date_format("claim_date", "yyyy-MM"))
        .filter(F.col("claim_id").isNotNull())
        .filter(F.col("claim_amount") > 0)
        .dropDuplicates(["claim_id"])
    )

    return (
        cleaned_claims.alias("c")
        .join(patients.alias("p"), "patient_id", "left")
        .join(providers.alias("pr"), "provider_id", "left")
        .join(diagnosis_codes.alias("d"), "diagnosis_code", "left")
        .select(
            "claim_id",
            "patient_id",
            F.concat_ws(" ", F.col("p.first_name"), F.col("p.last_name")).alias("patient_name"),
            F.col("p.gender").alias("patient_gender"),
            "provider_id",
            "provider_name",
            "provider_type",
            "network_status",
            "diagnosis_code",
            "diagnosis_description",
            "diagnosis_category",
            "claim_amount",
            "claim_date",
            "claim_month",
            "claim_status",
            F.col("c.insurance_plan").alias("insurance_plan"),
            F.col("c.state").alias("claim_state"),
        )
    )


def aggregate_claims(silver_claims: DataFrame) -> dict[str, DataFrame]:
    paid_or_approved = silver_claims.filter(F.col("claim_status").isin("approved", "paid"))

    return {
        "claim_kpi_summary": silver_claims.agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_submitted_amount"),
            F.round(
                F.sum(F.when(F.col("claim_status").isin("approved", "paid"), F.col("claim_amount")).otherwise(0.0)),
                2,
            ).alias("approved_paid_amount"),
            F.round(F.sum(F.when(F.col("claim_status") == "pending", F.col("claim_amount")).otherwise(0.0)), 2).alias(
                "pending_exposure"
            ),
            F.round(
                (F.countDistinct(F.when(F.col("claim_status") == "denied", F.col("claim_id"))) / F.countDistinct("claim_id"))
                * 100,
                2,
            ).alias("denial_rate_pct"),
            F.round(
                F.sum(
                    F.when(
                        (F.col("network_status") == "out_of_network")
                        & F.col("claim_status").isin("approved", "paid"),
                        F.col("claim_amount"),
                    ).otherwise(0.0)
                ),
                2,
            ).alias("out_of_network_approved_paid_amount"),
        ),
        "network_claims_summary": paid_or_approved.groupBy("network_status")
        .agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        )
        .orderBy("network_status"),
        "claims_by_provider": paid_or_approved.groupBy("provider_id", "provider_name", "provider_type")
        .agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
            F.round(F.avg("claim_amount"), 2).alias("avg_claim_amount"),
        )
        .orderBy(F.desc("total_claim_amount")),
        "claims_by_state": paid_or_approved.groupBy("claim_state")
        .agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        )
        .orderBy("claim_state"),
        "claims_by_diagnosis": paid_or_approved.groupBy("diagnosis_code", "diagnosis_description", "diagnosis_category")
        .agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        )
        .orderBy(F.desc("total_claim_amount")),
        "monthly_claims": paid_or_approved.groupBy("claim_month")
        .agg(
            F.countDistinct("claim_id").alias("claim_count"),
            F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        )
        .orderBy("claim_month"),
    }


def run_transformations(
    staging_dir: Path = STAGING_DIR,
    silver_dir: Path = SILVER_DIR,
    gold_dir: Path = GOLD_DIR,
) -> None:
    spark = create_spark()

    claims = read_csv(spark, staging_dir / "claims.csv")
    patients = read_csv(spark, staging_dir / "patients.csv")
    providers = read_csv(spark, staging_dir / "providers.csv")
    diagnosis_codes = read_csv(spark, staging_dir / "diagnosis_codes.csv")

    silver_claims = build_silver_claims(claims, patients, providers, diagnosis_codes)
    silver_claims.write.mode("overwrite").parquet(str(silver_dir / "claims_enriched"))

    for table_name, frame in aggregate_claims(silver_claims).items():
        frame.write.mode("overwrite").parquet(str(gold_dir / table_name))

    spark.stop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PySpark healthcare claims transformations.")
    parser.add_argument("--staging-dir", type=Path, default=STAGING_DIR)
    parser.add_argument("--silver-dir", type=Path, default=SILVER_DIR)
    parser.add_argument("--gold-dir", type=Path, default=GOLD_DIR)
    args = parser.parse_args()

    run_transformations(args.staging_dir, args.silver_dir, args.gold_dir)


if __name__ == "__main__":
    main()
