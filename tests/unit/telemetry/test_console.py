"""
Unit tests for ConsoleExporter.
"""

from __future__ import annotations

from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

from src.telemetry.exporters.console import ConsoleExporter


def test_console_exporter_creates_metric_reader() -> None:
    """
    Verify a MetricReader is created.
    """

    exporter = ConsoleExporter()

    reader = exporter.metric_reader()

    assert isinstance(
        reader,
        PeriodicExportingMetricReader,
    )


def test_console_exporter_accepts_custom_interval() -> None:
    """
    Verify custom export interval is accepted.
    """

    exporter = ConsoleExporter(
        export_interval_millis=1000,
    )

    reader = exporter.metric_reader()

    assert isinstance(
        reader,
        PeriodicExportingMetricReader,
    )