"""
OpenTelemetry MeterProvider configuration.

Purpose:
    Configure the OpenTelemetry Metrics SDK for PerfLens.

Responsibilities:
    - Configure MeterProvider.
    - Configure OpenTelemetry Resource.
    - Obtain MetricReaders from exporter implementations.
    - Expose Meter instances.

This module does NOT:
    - Record metrics.
    - Create instruments.
    - Know about the simulator.
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
from opentelemetry.sdk.resources import Resource

# ============================================================================
# Local Imports
# ============================================================================

from src.telemetry.exporters.factory import ExporterFactory


class TelemetryProvider:
    """
    Configures the OpenTelemetry Metrics SDK.
    """

    def __init__(
        self,
        service_name: str = "PerfLens",
        service_version: str = "1.0.0",
        exporter: str = "console",
        **exporter_kwargs,
    ) -> None:
        """
        Initialize the telemetry provider.

        Args:
            service_name:
                Service name reported to OpenTelemetry.

            service_version:
                Service version.

            exporter:
                Exporter implementation name.

            exporter_kwargs:
                Additional exporter-specific configuration.
        """

        resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": service_version,
            }
        )

        exporter_instance = ExporterFactory.create(
            exporter,
            **exporter_kwargs,
        )

        provider = MeterProvider(
            resource=resource,
            metric_readers=[
                exporter_instance.metric_reader(),
            ],
        )

        metrics.set_meter_provider(
            provider,
        )

        self._provider = provider

        self._meter = metrics.get_meter(
            name=service_name,
            version=service_version,
        )

    # ===================================================================

    @property
    def meter(self):
        """
        Return the configured Meter.
        """
        return self._meter

    # ===================================================================

    @property
    def provider(self) -> MeterProvider:
        """
        Return the configured MeterProvider.
        """
        return self._provider