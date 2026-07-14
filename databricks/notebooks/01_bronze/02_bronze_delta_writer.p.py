# Databricks notebook source
# MAGIC %run ./01_kafka_stream_reader.py

# COMMAND ----------

# Databricks notebook source
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

bronze_df = (
    stream_df.select(
        "topic",
        "partition",
        "offset",
        "timestamp",
        "timestampType",
        "key",
        "value"
    )
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
)

# COMMAND ----------

checkpoint_path = "/Volumes/workspace/default/perflens_checkpoints/bronze"

table_name = "workspace.default.bronze_telemetry_metrics_raw"

(
    bronze_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .toTable(table_name)
)

# COMMAND ----------

display(
    spark.sql("""
        SELECT *
        FROM workspace.default.bronze_telemetry_metrics_raw
        ORDER BY timestamp DESC
        LIMIT 1
    """)
)