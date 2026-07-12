"""
OTLP exporter implementation for the PerfLens telemetry subsystem.

Purpose:
    Create a MetricReader that exports metrics using the
    OpenTelemetry Protocol (OTLP) over HTTP.

Responsibilities:
    - Configure OTLPMetricExporter.
    - Configure PeriodicExportingMetricReader.

This module does NOT:
    - Configure MeterProvider.
    - Record metrics.
    - Know about the simulator.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# OpenTelemetry Imports
# ============================================================================

from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)

from opentelemetry.sdk.metrics.export import (
    MetricReader,
    PeriodicExportingMetricReader,
)

# ============================================================================
# Local Imports
# ============================================================================

from src.telemetry.exporters.base import BaseExporter


class OTLPExporter(BaseExporter):
    """
    OTLP metric exporter.
    """

    def __init__(
        self,
        endpoint: str = "http://localhost:4318/v1/metrics",
        headers: dict[str, str] | None = None,
        timeout: int = 10,
        export_interval_millis: int = 5000,
    ) -> None:
        """
        Initialize the OTLP exporter.
        """

        self._endpoint = endpoint

        self._headers = headers

        self._timeout = timeout

        self._export_interval_millis = (
            export_interval_millis
        )

    # ===============================================================

    def metric_reader(
        self,
    ) -> MetricReader:
        """
        Create a MetricReader.
        """

        exporter = OTLPMetricExporter(
            endpoint=self._endpoint,
            headers=self._headers,
            timeout=self._timeout,
        )

        return PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=self._export_interval_millis,
        )