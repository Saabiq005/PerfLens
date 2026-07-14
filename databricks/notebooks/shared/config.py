"""
Shared configuration for the PerfLens Databricks platform.
"""

KAFKA_BOOTSTRAP_SERVERS = (
    "perfLens.servicebus.windows.net:9093"
)

TOPIC = "perfLens.metrics"

EVENTHUB_CONNECTION_STRING = (
    "Endpoint=sb://perflens.servicebus.windows.net/;SharedAccessKeyName=perflens-databricks;SharedAccessKey=uqEl6wz1o6tYisNq8kxiSdSIyKTSowVFb+AEhGInoYQ=;EntityPath=perflens.metrics"
)

CHECKPOINT_ROOT = (
    "/tmp/perflens/checkpoints"
)

BRONZE_TABLE = (
    "workspace.default.bronze_telemetry_metrics_raw"
)

BRONZE_CHECKPOINT = (
    f"{CHECKPOINT_ROOT}/bronze"
)