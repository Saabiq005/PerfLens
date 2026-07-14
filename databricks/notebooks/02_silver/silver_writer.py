# Databricks notebook source
# MAGIC %run ./01_otlp_normalizer

# COMMAND ----------

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    LongType,
    TimestampType,
)

# COMMAND ----------

SILVER_SCHEMA = StructType([
StructField(
    "kafka_topic",
    StringType(),
    True,
),

StructField(
    "kafka_partition",
    LongType(),
    True,
),

StructField(
    "kafka_offset",
    LongType(),
    True,
),

StructField(
    "kafka_timestamp",
    TimestampType(),
    True,
),

StructField(
    "bronze_ingestion_timestamp",
    TimestampType(),
    True,
),
    # ------------------------------------------------------------------
    # Telemetry Resource
    # ------------------------------------------------------------------

    StructField(
        "telemetry_service_name",
        StringType(),
        True,
    ),

    StructField(
        "telemetry_service_version",
        StringType(),
        True,
    ),

    StructField(
        "telemetry_sdk_name",
        StringType(),
        True,
    ),

    StructField(
        "telemetry_sdk_language",
        StringType(),
        True,
    ),

    StructField(
        "telemetry_sdk_version",
        StringType(),
        True,
    ),

    StructField(
        "telemetry_instance_id",
        StringType(),
        True,
    ),

    # ------------------------------------------------------------------
    # Observed Service
    # ------------------------------------------------------------------

    StructField(
        "observed_service_id",
        StringType(),
        True,
    ),

    StructField(
        "observed_service_name",
        StringType(),
        True,
    ),

    StructField(
        "observed_service_version",
        StringType(),
        True,
    ),

    StructField(
        "deployment_environment",
        StringType(),
        True,
    ),

    # ------------------------------------------------------------------
    # Scenario
    # ------------------------------------------------------------------

    StructField(
        "scenario_id",
        StringType(),
        True,
    ),

    StructField(
        "scenario_name",
        StringType(),
        True,
    ),

    StructField(
        "scenario_description",
        StringType(),
        True,
    ),

    # ------------------------------------------------------------------
    # Metric
    # ------------------------------------------------------------------

    StructField(
        "metric_name",
        StringType(),
        True,
    ),

    StructField(
        "metric_description",
        StringType(),
        True,
    ),

    StructField(
        "metric_type",
        StringType(),
        True,
    ),

    StructField(
        "metric_unit",
        StringType(),
        True,
    ),

    StructField(
        "metric_value",
        DoubleType(),
        True,
    ),

    # ------------------------------------------------------------------
    # Histogram Statistics
    # ------------------------------------------------------------------

    StructField(
        "histogram_count",
        LongType(),
        True,
    ),

    StructField(
        "histogram_sum",
        DoubleType(),
        True,
    ),

    StructField(
        "histogram_min",
        DoubleType(),
        True,
    ),

    StructField(
        "histogram_max",
        DoubleType(),
        True,
    ),

    # ------------------------------------------------------------------
    # Time
    # ------------------------------------------------------------------

    StructField(
        "event_timestamp",
        TimestampType(),
        True,
    ),

    StructField(
        "collection_start_timestamp",
        TimestampType(),
        True,
    ),
])

# COMMAND ----------

bronze_df = spark.table(
    "workspace.default.bronze_telemetry_metrics_raw"
)

# COMMAND ----------

bronze_rows = (
    bronze_df
        .select(
            "topic",
            "partition",
            "offset",
            "timestamp",
            "ingestion_timestamp",
            "value",
        )
        .collect()
)

# COMMAND ----------

records = []

for row in bronze_rows:

    context = {

        "kafka_topic":
            row.topic,

        "kafka_partition":
            row.partition,

        "kafka_offset":
            row.offset,

        "kafka_timestamp":
            row.timestamp,

        "bronze_ingestion_timestamp":
            row.ingestion_timestamp,
    }

    records.extend(
        normalize_metrics(
            payload=row.value,
            context=context,
        )
    )

# COMMAND ----------

silver_df = spark.createDataFrame(
    records,
    schema=SILVER_SCHEMA,
)


# COMMAND ----------

(
    silver_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(
            "workspace.default.silver_telemetry_metrics"
        )
)

# COMMAND ----------

display(
    spark.table(
        "workspace.default.silver_telemetry_metrics"
    )
)