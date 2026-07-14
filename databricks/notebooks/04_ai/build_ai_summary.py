# Databricks notebook source
pip install google-genai

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

# Databricks notebook source

from pyspark.sql import functions as F

SILVER_TABLE = "workspace.default.silver_telemetry_metrics"

silver_df = spark.table(SILVER_TABLE)

# COMMAND ----------

# Databricks notebook source

from pyspark.sql import functions as F

SILVER_TABLE = "workspace.default.silver_telemetry_metrics"

silver_df = spark.table(SILVER_TABLE)

# COMMAND ----------

latency_df = (

    silver_df

    .filter(
        F.col("metric_name") == "latency"
    )

    .groupBy(

        "observed_service_name",

        "scenario_name"

    )

    .agg(

        F.avg("histogram_sum").alias("avg_latency"),

        F.max("histogram_max").alias("max_latency"),

        F.min("histogram_min").alias("min_latency"),

        F.avg("histogram_count").alias("sample_count")

    )

)

# COMMAND ----------

throughput_df = (

    silver_df

    .filter(
        F.col("metric_name") == "throughput"
    )

    .groupBy(

        "observed_service_name",

        "scenario_name"

    )

    .agg(

        F.avg("metric_value").alias("avg_throughput")

    )

)

# COMMAND ----------

throughput_df = (

    silver_df

    .filter(
        F.col("metric_name") == "throughput"
    )

    .groupBy(

        "observed_service_name",

        "scenario_name"

    )

    .agg(

        F.avg("metric_value").alias("avg_throughput")

    )

)

# COMMAND ----------

error_df = (

    silver_df

    .filter(
        F.col("metric_name") == "error_rate"
    )

    .groupBy(

        "observed_service_name",

        "scenario_name"

    )

    .agg(

        F.avg("metric_value").alias("avg_error_rate")

    )

)

# COMMAND ----------

summary_df = (

    latency_df

    .join(

        throughput_df,

        [

            "observed_service_name",

            "scenario_name"

        ]

    )

    .join(

        error_df,

        [

            "observed_service_name",

            "scenario_name"

        ]

    )

)

# COMMAND ----------

summary_df = (

    summary_df

    .withColumn(
        "avg_latency",
        F.round("avg_latency",2)
    )

    .withColumn(
        "max_latency",
        F.round("max_latency",2)
    )

    .withColumn(
        "min_latency",
        F.round("min_latency",2)
    )

    .withColumn(
        "avg_throughput",
        F.round("avg_throughput",2)
    )

    .withColumn(
        "avg_error_rate",
        F.round("avg_error_rate",4)
    )

)

# COMMAND ----------

display(summary_df)

# COMMAND ----------

from google import genai
import json

# COMMAND ----------
"""
client = genai.Client(
    api_key="******"
)
"""
# COMMAND ----------

summary = [

    row.asDict()

    for row in summary_df.collect()

]

summary_json = json.dumps(
    summary,
    indent=2,
    default=str
)

# COMMAND ----------

BASELINE = """
You are the AI Performance Analysis Engine for PerfLens.

PerfLens simulates enterprise application performance under different scenarios.

Expected operating behaviour

Healthy Operation
- Latency 90-110 ms
- Throughput 230-260 req/s
- Error Rate below 1%

Traffic Spike
- Latency moderately increased
- Throughput reduced
- Error Rate below 3%

Database Bottleneck
- Latency high
- Throughput significantly reduced
- Error Rate may increase

Recovery
- Metrics should move back toward Healthy values.

Error Storm
- Error Rate very high.
- Throughput reduced.
- Latency may increase.

For every record:

1. Compare observed metrics with expected behaviour.

2. Determine if regression exists.

3. Explain probable root cause.

4. Recommend corrective action.

Return ONLY valid JSON.

Schema:

[
{
"service":"",
"scenario":"",
"system_health":"",
"severity":"",
"regression_detected":true,
"root_cause":"",
"recommendation":"",
"confidence":0.0
}
]
"""

# COMMAND ----------

PROMPT = f"""

{BASELINE}

Performance summaries

{summary_json}

"""

# COMMAND ----------

response = client.models.generate_content(

    model="models/gemini-3.5-flash",

    contents=PROMPT

)

# COMMAND ----------

response_text = response.text.strip()

response_text = (
    response_text
    .replace("```json","")
    .replace("```","")
    .strip()
)

annotations = json.loads(response_text)

# COMMAND ----------

annotation_df = spark.createDataFrame(
    annotations
)

display(annotation_df)

# COMMAND ----------

annotation_df = (

    annotation_df

    .withColumnRenamed(
        "service",
        "observed_service_name"
    )

    .withColumnRenamed(
        "scenario",
        "scenario_name"
    )

)

# COMMAND ----------

print(annotation_df.columns)

# COMMAND ----------

gold_ai_df = (
    summary_df
        .join(
            annotation_df,
            [
                "observed_service_name",
                "scenario_name"
            ],
            "inner"
        )
)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

# COMMAND ----------

gold_ai_df = (

    gold_ai_df

    .withColumn(

        "analysis_timestamp",

        current_timestamp()

    )

)

# COMMAND ----------

(
    gold_ai_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(
            "workspace.default.gold_ai_annotations"
        )
)

# COMMAND ----------

display(
spark.table(
"workspace.default.gold_ai_annotations"
)
)