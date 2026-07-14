# Databricks notebook source
# Databricks notebook source

# ============================================================================
# Imports
# ============================================================================

from __future__ import annotations

from datetime import datetime
from datetime import timezone

from opentelemetry.proto.metrics.v1.metrics_pb2 import MetricsData


# ============================================================================
# Generic Helpers
# ============================================================================

def parse_any_value(any_value):
    """
    Convert an OpenTelemetry AnyValue into a native Python object.
    """

    field = any_value.WhichOneof("value")

    if field is None:
        return None

    return getattr(any_value, field)


def unix_nano_to_datetime(
    unix_nano: int,
):
    """
    Convert Unix nanoseconds to UTC datetime.
    """

    return datetime.fromtimestamp(
        unix_nano / 1_000_000_000,
        tz=timezone.utc,
    )


# ============================================================================
# Attribute Extraction
# ============================================================================

def extract_attributes(
    attributes,
) -> dict[str, object]:
    """
    Convert OTLP KeyValue attributes into a Python dictionary.
    """

    values = {}

    for attribute in attributes:

        values[attribute.key] = parse_any_value(
            attribute.value
        )

    return values


# ============================================================================
# Resource Extraction
# ============================================================================

def extract_resource_fields(
    resource_attributes: dict,
) -> dict:
    """
    Extract telemetry resource fields.
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


# ============================================================================
# Metric Attribute Extraction
# ============================================================================

def extract_metric_fields(
    metric_attributes: dict,
) -> dict:
    """
    Extract observed service and scenario fields.
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


# ============================================================================
# Histogram Normalizer
# ============================================================================

def normalize_histogram(
    metric,
    resource_attributes,
    context,
):
    """
    Normalize one histogram metric.
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

            **context,

            **resource_fields,

            **metric_fields,

            "metric_name":
                metric.name,

            "metric_description":
                metric.description,

            "metric_unit":
                metric.unit,

            "metric_type":
                "histogram",

            "metric_value":
                None,

            "histogram_count":
                data_point.count,

            "histogram_sum":
                data_point.sum,

            "histogram_min":
                data_point.min,

            "histogram_max":
                data_point.max,

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


# ============================================================================
# Sum Normalizer
# ============================================================================

def normalize_sum(
    metric,
    resource_attributes,
    context,
):
    """
    Normalize one sum metric.
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

        value = (
            data_point.as_double
            if data_point.HasField("as_double")
            else float(data_point.as_int)
        )

        record = {

            **context,

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
                value,

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


# ============================================================================
# Gauge Normalizer
# ============================================================================

def normalize_gauge(
    metric,
    resource_attributes,
    context,
):
    """
    Normalize one gauge metric.
    """

    records = []

    for data_point in metric.gauge.data_points:

        metric_attributes = extract_attributes(
            data_point.attributes
        )

        resource_fields = extract_resource_fields(
            resource_attributes
        )

        metric_fields = extract_metric_fields(
            metric_attributes
        )

        value = (
            data_point.as_double
            if data_point.HasField("as_double")
            else float(data_point.as_int)
        )

        record = {

            **context,

            **resource_fields,

            **metric_fields,

            "metric_name":
                metric.name,

            "metric_description":
                metric.description,

            "metric_unit":
                metric.unit,

            "metric_type":
                "gauge",

            "metric_value":
                value,

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


# ============================================================================
# Public API
# ============================================================================

def normalize_metrics(
    payload: bytes,
    context: dict,
) -> list[dict]:
    """
    Normalize one OTLP Metrics payload into analytical records.
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

                match metric_type:

                    case "histogram":

                        records.extend(
                            normalize_histogram(
                                metric,
                                resource_attributes,
                                context,
                            )
                        )

                    case "sum":

                        records.extend(
                            normalize_sum(
                                metric,
                                resource_attributes,
                                context,
                            )
                        )

                    case "gauge":

                        records.extend(
                            normalize_gauge(
                                metric,
                                resource_attributes,
                                context,
                            )
                        )

                    case _:

                        print(
                            f"Unsupported metric type: {metric_type}"
                        )

    return records