"""
OpenTelemetry MeterProvider configuration.

Purpose:
    Configure the OpenTelemetry Metrics SDK for PerfLens.

Responsibilities:
    - Configure MeterProvider.
    - Configure MetricReader.
    - Configure Exporter.
    - Expose Meter instances.

This module does NOT:
    - Create instruments.
    - Record metrics.
    - Know about simulation.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# OpenTelemetry Imports
# ============================================================================

from opentelemetry import metrics

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

from opentelemetry.sdk.resources import Resource


class TelemetryProvider:
    """
    Configures the OpenTelemetry Metrics SDK.
    """

    def __init__(
        self,
        service_name: str = "PerfLens",
        service_version: str = "1.0.0",
    ) -> None:

        resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": service_version,
            }
        )

        exporter = ConsoleMetricExporter()

        reader = PeriodicExportingMetricReader(
            exporter,
        )

        provider = MeterProvider(
            resource=resource,
            metric_readers=[
                reader,
            ],
        )

        metrics.set_meter_provider(
            provider,
        )

        self._meter = metrics.get_meter(
            "PerfLens",
            service_version,
        )

    @property
    def meter(self):
        """
        Return the configured Meter.
        """
        return self._meter