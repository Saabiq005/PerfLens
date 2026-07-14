# Databricks notebook source
# Databricks notebook source

# ============================================================================
# PerfLens - Bronze Kafka Stream Reader
# ============================================================================

KAFKA_BOOTSTRAP_SERVERS = (
    "perfLens.servicebus.windows.net:9093"
)

TOPIC = "perfLens.metrics"

EVENTHUB_CONNECTION_STRING = (
    "Endpoint=sb://perflens.servicebus.windows.net/;SharedAccessKeyName=perflens-databricks;SharedAccessKey=uqEl6wz1o6tYisNq8kxiSdSIyKTSowVFb+AEhGInoYQ=;EntityPath=perflens.metrics")

# COMMAND ----------

kafka_options = {

    "kafka.bootstrap.servers":
        KAFKA_BOOTSTRAP_SERVERS,

    "subscribe":
        TOPIC,

    "startingOffsets":
        "earliest",

    "kafka.security.protocol":
        "SASL_SSL",

    "kafka.sasl.mechanism":
        "PLAIN",

    "kafka.sasl.jaas.config":
        (
            'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required '
            'username="$ConnectionString" '
            f'password="{EVENTHUB_CONNECTION_STRING}";'
        )
}

# COMMAND ----------

stream_df = (
    spark.readStream
         .format("kafka")
         .options(**kafka_options)
         .load()
)