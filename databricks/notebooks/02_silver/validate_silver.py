# Databricks notebook source
# MAGIC %run ./01_otlp_normalizer

# COMMAND ----------

bronze_df = spark.table(
    "workspace.default.bronze_telemetry_metrics_raw"
)

payload = (
    bronze_df
        .select("value")
        .limit(1)
        .collect()[0]
        .value
)

records = normalize_metrics(payload)

# COMMAND ----------

records = normalize_metrics(payload)

len(records)

records[0]

# COMMAND ----------

records = normalize_metrics(payload)

len(records)

records[0]

# COMMAND ----------

metric_counts = {}

for record in records:

    name = record["metric_name"]

    metric_counts[name] = (
        metric_counts.get(name, 0) + 1
    )

metric_counts