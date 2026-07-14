# Databricks notebook source
# Databricks notebook source

# ============================================================================
# Imports
# ============================================================================

from pyspark.sql import functions as F


# ============================================================================
# Configuration
# ============================================================================

BRONZE_TABLE = "workspace.default.bronze_telemetry_metrics_raw"

SILVER_TABLE = "workspace.default.silver_telemetry_metrics"

EXPECTED_METRICS = {
    "latency",
    "throughput",
    "error_rate",
    "trace_duration",
}

EXPECTED_SCENARIOS = {
    "Healthy Operation",
    "Traffic Spike",
    "Database Bottleneck",
    "Recovery",
    "Error Storm",
}

validation_results = []

# COMMAND ----------

# ============================================================================
# Bronze Validation
# ============================================================================

print("=" * 80)
print("BRONZE VALIDATION")
print("=" * 80)

# Bronze table exists

bronze_exists = spark.catalog.tableExists(BRONZE_TABLE)

validation_results.append(
    ("Bronze Table Exists", bronze_exists)
)

if bronze_exists:

    bronze_df = spark.table(BRONZE_TABLE)

    bronze_count = bronze_df.count()

    validation_results.append(
        ("Bronze Record Count > 0", bronze_count > 0)
    )

    duplicate_offsets = (
        bronze_df
            .groupBy(
                "topic",
                "partition",
                "offset"
            )
            .count()
            .filter("count > 1")
            .count()
    )

    validation_results.append(
        ("Duplicate Kafka Offsets", duplicate_offsets == 0)
    )

    null_payloads = (
        bronze_df
            .filter(F.col("value").isNull())
            .count()
    )

    validation_results.append(
        ("Null Payload Check", null_payloads == 0)
    )

# COMMAND ----------

# ============================================================================
# Silver Validation
# ============================================================================

print("=" * 80)
print("SILVER VALIDATION")
print("=" * 80)

silver_exists = spark.catalog.tableExists(SILVER_TABLE)

validation_results.append(
    ("Silver Table Exists", silver_exists)
)

if silver_exists:

    silver_df = spark.table(SILVER_TABLE)

    silver_count = silver_df.count()

    validation_results.append(
        ("Silver Record Count > 0", silver_count > 0)
    )

    # ----------------------------------------------------------------------
    # Metric Coverage
    # ----------------------------------------------------------------------

    metrics_found = {
        row.metric_name
        for row in silver_df.select("metric_name").distinct().collect()
    }

    validation_results.append(
        (
            "Metric Coverage",
            EXPECTED_METRICS.issubset(metrics_found)
        )
    )

    # ----------------------------------------------------------------------
    # Scenario Coverage
    # ----------------------------------------------------------------------

    scenarios_found = {
        row.scenario_name
        for row in silver_df.select("scenario_name").distinct().collect()
    }

    validation_results.append(
        (
            "Scenario Coverage",
            EXPECTED_SCENARIOS.issubset(scenarios_found)
        )
    )

    # ----------------------------------------------------------------------
    # Critical Null Check
    # ----------------------------------------------------------------------

    null_count = (
        silver_df
        .filter(

            F.col("metric_name").isNull()

            | F.col("observed_service_name").isNull()

            | F.col("scenario_name").isNull()

        )
        .count()
    )

    validation_results.append(
        (
            "Critical Null Check",
            null_count == 0
        )
    )

    # ----------------------------------------------------------------------
    # Histogram Sanity
    # ----------------------------------------------------------------------

    histogram_errors = (

        silver_df

        .filter(
            (F.col("metric_type") == "histogram")
            &
            (F.col("histogram_min") > F.col("histogram_max"))
        )

        .count()

    )

    validation_results.append(
        (
            "Histogram Sanity",
            histogram_errors == 0
        )
    )

    # ----------------------------------------------------------------------
    # Kafka Lineage
    # ----------------------------------------------------------------------

    lineage_errors = (

        silver_df

        .filter(

            F.col("kafka_topic").isNull()

            | F.col("kafka_partition").isNull()

            | F.col("kafka_offset").isNull()

        )

        .count()

    )

    validation_results.append(
        (
            "Kafka Lineage",
            lineage_errors == 0
        )
    )

# COMMAND ----------

# ============================================================================
# Validation Summary
# ============================================================================

print()
print("=" * 80)
print("PERFLENS DATA QUALITY REPORT")
print("=" * 80)

overall_status = True

for check_name, passed in validation_results:

    overall_status &= passed

    print(
        f"{check_name:<45}"
        f"{'PASS' if passed else 'FAIL'}"
    )

print("=" * 80)

print(
    f"{'OVERALL STATUS':<45}"
    f"{'PASS' if overall_status else 'FAIL'}"
)

print("=" * 80)

# COMMAND ----------

# ============================================================================
# Bronze Sample
# ============================================================================

display(
    spark.table(BRONZE_TABLE)
)

# COMMAND ----------

# ============================================================================
# Silver Sample
# ============================================================================

display(
    spark.table(SILVER_TABLE)
)