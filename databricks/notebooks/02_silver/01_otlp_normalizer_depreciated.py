# Databricks notebook source
# Databricks notebook source

from __future__ import annotations

from google.protobuf.message import Message
from opentelemetry.proto.metrics.v1.metrics_pb2 import MetricsData
from datetime import datetime, timezone

# COMMAND ----------

def parse_any_value(any_value):
    """
    Convert an OTLP AnyValue into a native Python value.
    """

    field = any_value.WhichOneof("value")

    if field is None:
        return None

    return getattr(any_value, field)

# COMMAND ----------

def extract_attributes(attributes) -> dict[str, object]:
    """
    Convert OTLP KeyValue attributes into a Python dictionary.
    """

    values = {}

    for attribute in attributes:

        values[attribute.key] = parse_any_value(
            attribute.value
        )

    return values

# COMMAND ----------

def unix_nano_to_datetime(
    unix_nano: int,
):
    """
    Convert OTLP nanoseconds to UTC datetime.
    """

    return datetime.fromtimestamp(
        unix_nano / 1_000_000_000,
        tz=timezone.utc,
    )

# COMMAND ----------

def extract_resource_fields(
    resource_attributes: dict,
) -> dict:
    """
    Extract normalized resource fields.
    """

    return {

        "telemetry_service_name":
            resource_attributes.get("service.name"),

        "telemetry_service_version":
            resource_attributes.get("service.version"),

        "telemetry_sdk_name":
            resource_attributes.get("telemetry.sdk.name"),

        "telemetry_sdk_language":
            resource_attributes.get("telemetry.sdk.language"),

        "telemetry_sdk_version":
            resource_attributes.get("telemetry.sdk.version"),

        "telemetry_instance_id":
            resource_attributes.get("service.instance.id"),
    }

# COMMAND ----------

def extract_metric_fields(
    metric_attributes: dict,
) -> dict:
    """
    Extract normalized metric attribute fields.
    """

    return {

        "observed_service_id":
            metric_attributes.get("service.id"),

        "observed_service_name":
            metric_attributes.get("service.name"),

        "observed_service_version":
            metric_attributes.get("service.version"),

        "deployment_environment":
            metric_attributes.get(
                "deployment.environment"
            ),

        "scenario_id":
            metric_attributes.get("scenario.id"),

        "scenario_name":
            metric_attributes.get("scenario.name"),

        "scenario_description":
            metric_attributes.get(
                "scenario.description"
            ),
    }

# COMMAND ----------

def normalize_histogram(
    metric,
    resource_attributes,
):
    """
    Normalize one OTLP histogram metric.

    Returns
    -------
    list[dict]
        One dictionary per HistogramDataPoint.
    """

    records = []

    for data_point in metric.histogram.data_points:

        metric_attributes = extract_attributes(
            data_point.attributes
        )

        resource_fields = extract_resource_fields(
            resource_attributes
        )

        metric_fields = extract_metric_fields(
            metric_attributes
        )

        record = {
            **resource_fields,
            **metric_fields,
            "metric_name": metric.name,
            "metric_description": metric.description,
            "metric_unit": metric.unit,
            "metric_type": "histogram",
            "histogram_count": data_point.count,
            "histogram_sum": data_point.sum,
            "histogram_min": data_point.min,
            "histogram_max": data_point.max,
            "metric_value": None,
            "event_timestamp": unix_nano_to_datetime(
                data_point.time_unix_nano
            ),
            "collection_start_timestamp": unix_nano_to_datetime(
                data_point.start_time_unix_nano
            ),
        }

        records.append(record)

    return records

# COMMAND ----------

def normalize_sum(
    metric,
    resource_attributes,
):
    """
    Normalize one OTLP Sum metric.
    """

    records = []

    for data_point in metric.sum.data_points:

        metric_attributes = extract_attributes(
            data_point.attributes
        )

        resource_fields = extract_resource_fields(
            resource_attributes
        )

        metric_fields = extract_metric_fields(
            metric_attributes
        )

        record = {

            **resource_fields,

            **metric_fields,

            "metric_name":
                metric.name,

            "metric_description":
                metric.description,

            "metric_unit":
                metric.unit,

            "metric_type":
                "sum",

            "metric_value":
                data_point.as_double
                if data_point.HasField("as_double")
                else float(data_point.as_int),

            "histogram_count":
                None,

            "histogram_sum":
                None,

            "histogram_min":
                None,

            "histogram_max":
                None,

            "event_timestamp":
                unix_nano_to_datetime(
                    data_point.time_unix_nano
                ),

            "collection_start_timestamp":
                unix_nano_to_datetime(
                    data_point.start_time_unix_nano
                ),
        }

        records.append(record)

    return records

# COMMAND ----------


def normalize_gauge(
    metric,
    resource_attributes,
):
    return []

# COMMAND ----------

def normalize_metrics(
    payload: bytes,
) -> list[dict]:
    """
    Normalize one OTLP Metrics payload.
    """

    metrics = MetricsData()

    metrics.ParseFromString(payload)

    records = []

    for resource_metrics in metrics.resource_metrics:

        resource_attributes = extract_attributes(
            resource_metrics.resource.attributes
        )

        for scope_metrics in resource_metrics.scope_metrics:

            for metric in scope_metrics.metrics:

                metric_type = metric.WhichOneof("data")

                print(f"{metric.name} -> {metric_type}")

                match metric_type:

                    case "histogram":

                        records.extend(
                            normalize_histogram(
                                metric,
                                resource_attributes,
                            )
                        )

                    case "sum":

                        records.extend(
                            normalize_sum(
                                metric,
                                resource_attributes,
                            )
                        )

                    case "gauge":

                        records.extend(
                            normalize_gauge(
                                metric,
                                resource_attributes,
                            )
                        )

                    case _:

                        print(
                            f"Unsupported metric type: {metric_type}"
                        )

    return records