# Databricks notebook source
# -------------------------------------------------------------------------
# CREDENTIAL CONFIGURATION (Match these with your local .env values)
# -------------------------------------------------------------------------
EVENTHUB_NAMESPACE = "perflens" 
EVENTHUB_NAME = "perflens.metrics"
TOPIC_NAME = "perflens.metrics"
# Use the full connection string ending with your primary key
EVENTHUB_CONNECTION_STRING = "Endpoint=sb://perflens.servicebus.windows.net/;SharedAccessKeyName=perflens-databricks;SharedAccessKey=uqEl6wz1o6tYisNq8kxiSdSIyKTSowVFb+AEhGInoYQ=;EntityPath=perflens.metrics"


# Construct endpoints
bootstrap_server = f"{EVENTHUB_NAMESPACE}.servicebus.windows.net:9093"
jaas_config = f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{EVENTHUB_CONNECTION_STRING}";'

# Explicit temporary location in the local Databricks File System (DBFS)
TEMP_CHECKPOINT_PATH = "dbfs:/tmp/perflens/stream_preview_checkpoint"

# COMMAND ----------

raw_stream_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", bootstrap_server)
    .option("kafka.security.protocol", "SASL_SSL")
    .option("kafka.sasl.mechanism", "PLAIN")
    .option("kafka.sasl.jaas.config", jaas_config)
    .option("subscribe", TOPIC_NAME)
    .option("startingOffsets", "latest")
    .load())

# COMMAND ----------

# Convert the binary Kafka keys and values to strings so they are readable
readable_stream_df = raw_stream_df.selectExpr(
    "CAST(key AS STRING) as kafka_key",
    "CAST(value AS STRING) as raw_payload",
    "topic",
    "partition",
    "offset",
    "timestamp"
)

# Clear any previous checkpoint metadata to ensure a fresh, clean start
dbutils.fs.rm(TEMP_CHECKPOINT_PATH, recurse=True)

# Display the real-time updating stream by supplying the mandatory checkpoint path
display(readable_stream_df, checkpointLocation=TEMP_CHECKPOINT_PATH)

# COMMAND ----------

from pyspark.sql.functions import col, current_timestamp

# Add internal processing ingestion metadata timestamps for audit trails
bronze_df = raw_metrics_stream.select(
    col("key").cast("string").alias("kafka_key"),
    col("value").cast("binary").alias("raw_payload"),  # OTLP Protobuf bytes
    col("topic").cast("string"),
    col("partition").cast("int"),
    col("offset").cast("long"),
    col("timestamp").alias("kafka_timestamp"),
    current_timestamp().alias("ingested_timestamp")
)

# COMMAND ----------

# Create a schema and volume to act as your directory space
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.default")
spark.sql("CREATE VOLUME IF NOT EXISTS workspace.default.perflens_checkpoints")

# COMMAND ----------

# 1. Point to a brand new, clean subfolder to clear the corrupted metadata state
VOLUME_CHECKPOINT_PATH = "/Volumes/workspace/default/perflens_checkpoints/stream_preview_v6"

# 2. Read the Kafka engine stream
raw_stream_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", bootstrap_server)
    .option("kafka.security.protocol", "SASL_SSL")
    .option("kafka.sasl.mechanism", "PLAIN")
    .option("kafka.sasl.jaas.config", jaas_config)
    .option("subscribe", TOPIC_NAME)
    .option("startingOffsets", "earliest")
    .load())

# 3. Format binary columns into human-readable strings
readable_stream_df = raw_stream_df.selectExpr(
    "CAST(key AS STRING) as kafka_key",
    "CAST(value AS STRING) as raw_payload",
    "topic",
    "partition",
    "offset",
    "timestamp"
)


# COMMAND ----------


# 4. Render the preview using the fresh directory (let display handle the mode automatically)
display(readable_stream_df, checkpointLocation=VOLUME_CHECKPOINT_PATH)