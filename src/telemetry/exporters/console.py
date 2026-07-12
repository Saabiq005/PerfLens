"""
Console exporter implementation for the PerfLens telemetry subsystem.

Purpose:
    Create a MetricReader that exports metrics to the console.

Responsibilities:
    - Configure ConsoleMetricExporter.
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

from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    MetricReader,
    PeriodicExportingMetricReader,
)

# ============================================================================
# Local Imports
# ============================================================================

from src.telemetry.exporters.base import BaseExporter


class ConsoleExporter(BaseExporter):
    """
    OpenTelemetry console exporter.
    """

    def __init__(
        self,
        export_interval_millis: int = 5000,
    ) -> None:
        """
        Initialize the console exporter.

        Args:
            export_interval_millis:
                Export interval in milliseconds.
        """

        self._export_interval_millis = export_interval_millis

    def metric_reader(
        self,
    ) -> MetricReader:
        """
        Create a console MetricReader.

        Returns:
            Configured MetricReader.
        """

        exporter = ConsoleMetricExporter()

        return PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=self._export_interval_millis,
        )