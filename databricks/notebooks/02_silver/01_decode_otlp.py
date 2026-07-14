# Databricks notebook source
from opentelemetry.proto.metrics.v1.metrics_pb2 import MetricsData

# COMMAND ----------

bronze_df = spark.table(
    "workspace.default.bronze_telemetry_metrics_raw"
)

# COMMAND ----------

payload = (
    bronze_df
        .select("value")
        .limit(1)
        .collect()[0]
        .value
)

# COMMAND ----------

metrics = MetricsData()

metrics.ParseFromString(payload)

# COMMAND ----------

print(metrics)

# COMMAND ----------

metrics = MetricsData()
metrics.ParseFromString(payload)

# COMMAND ----------

for resource_metrics in metrics.resource_metrics:
    print(resource_metrics.resource)

# COMMAND ----------

for rm in metrics.resource_metrics:
    for sm in rm.scope_metrics:
        print(sm)

# COMMAND ----------

for rm in metrics.resource_metrics:
    for sm in rm.scope_metrics:
        for metric in sm.metrics:
            print(metric)

# COMMAND ----------

for resource_metrics in metrics.resource_metrics:
    print("=" * 80)
    print("RESOURCE")
    print("=" * 80)

    for scope_metrics in resource_metrics.scope_metrics:
        print(scope_metrics)