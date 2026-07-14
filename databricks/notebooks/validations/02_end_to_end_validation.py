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

validation_results = []

# COMMAND ----------

# ============================================================================
# Bronze Pipeline Validation
# ============================================================================

print("=" * 80)
print("BRONZE PIPELINE VALIDATION")
print("=" * 80)

bronze_df = spark.table(BRONZE_TABLE)

bronze_count = bronze_df.count()

validation_results.append(
    (
        "Bronze Table Populated",
        bronze_count > 0
    )
)

latest_offset = (

    bronze_df

    .agg(
        F.max("offset").alias("latest")
    )

    .collect()[0]["latest"]

)

validation_results.append(
    (
        "Kafka Offsets Available",
        latest_offset is not None
    )
)

payload_count = (

    bronze_df

    .filter(
        F.col("value").isNotNull()
    )

    .count()

)

validation_results.append(
    (
        "OTLP Payload Available",
        payload_count > 0
    )
)

# COMMAND ----------

# ============================================================================
# Silver Pipeline Validation
# ============================================================================

print("=" * 80)
print("SILVER PIPELINE VALIDATION")
print("=" * 80)

silver_df = spark.table(SILVER_TABLE)

silver_count = silver_df.count()

validation_results.append(
    (
        "Silver Table Populated",
        silver_count > 0
    )
)

metrics = (
    silver_df
        .select("metric_name")
        .distinct()
        .count()
)

validation_results.append(
    (
        "Metric Normalization",
        metrics >= 4
    )
)

services = (
    silver_df
        .select("observed_service_name")
        .distinct()
        .count()
)

validation_results.append(
    (
        "Observed Services",
        services > 0
    )
)

scenarios = (
    silver_df
        .select("scenario_name")
        .distinct()
        .count()
)

validation_results.append(
    (
        "Scenario Coverage",
        scenarios > 0
    )
)

# COMMAND ----------

# ============================================================================
# Pipeline Integrity
# ============================================================================

histograms = (

    silver_df

    .filter(
        F.col("metric_type") == "histogram"
    )

    .count()

)

validation_results.append(
    (
        "Histogram Metrics",
        histograms > 0
    )
)

sums = (

    silver_df

    .filter(
        F.col("metric_type") == "sum"
    )

    .count()

)

validation_results.append(
    (
        "Sum Metrics",
        sums > 0
    )
)

lineage = (

    silver_df

    .filter(

        F.col("kafka_offset").isNotNull()

    )

    .count()

)

validation_results.append(
    (
        "Kafka Lineage",
        lineage == silver_count
    )
)

timestamps = (

    silver_df

    .filter(
        F.col("event_timestamp").isNotNull()
    )

    .count()

)

validation_results.append(
    (
        "Event Timestamp",
        timestamps == silver_count
    )
)

# COMMAND ----------

# ============================================================================
# Summary
# ============================================================================

print()

print("=" * 80)
print("PERFLENS END-TO-END VALIDATION REPORT")
print("=" * 80)

overall = True

for name, status in validation_results:

    overall &= status

    print(
        f"{name:<45}"
        f"{'PASS' if status else 'FAIL'}"
    )

print("=" * 80)

print(
    f"{'OVERALL STATUS':<45}"
    f"{'PASS' if overall else 'FAIL'}"
)

print("=" * 80)

# COMMAND ----------

display(

spark.sql("""

SELECT

topic,

partition,

COUNT(*) records,

MAX(offset) latest_offset

FROM workspace.default.bronze_telemetry_metrics_raw

GROUP BY

topic,

partition

ORDER BY

partition

""")
)

# COMMAND ----------

display(

spark.sql("""

SELECT

metric_name,

metric_type,

COUNT(*) records,

COUNT(DISTINCT scenario_name) scenarios,

COUNT(DISTINCT observed_service_name) services

FROM workspace.default.silver_telemetry_metrics

GROUP BY

metric_name,

metric_type

ORDER BY

metric_name

""")
)

# COMMAND ----------

display(

spark.sql("""

SELECT

observed_service_name,

COUNT(*) records

FROM workspace.default.silver_telemetry_metrics

GROUP BY

observed_service_name

ORDER BY

records DESC

""")
)

# COMMAND ----------

display(

spark.sql("""

SELECT *

FROM workspace.default.silver_telemetry_metrics

ORDER BY

event_timestamp DESC

LIMIT 25

""")
)