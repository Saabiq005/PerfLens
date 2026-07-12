"""
Unit tests for ExporterFactory.
"""

from __future__ import annotations

import pytest

from src.telemetry.exporters.base import BaseExporter
from src.telemetry.exporters.console import ConsoleExporter
from src.telemetry.exporters.factory import ExporterFactory


def test_create_console_exporter() -> None:
    """
    Verify console exporter is created.
    """

    exporter = ExporterFactory.create(
        "console",
    )

    assert isinstance(
        exporter,
        ConsoleExporter,
    )


def test_supported_exporters() -> None:
    """
    Verify supported exporters are returned.
    """

    exporters = ExporterFactory.supported_exporters()

    assert "console" in exporters


def test_unknown_exporter_raises_error() -> None:
    """
    Verify unknown exporter raises ValueError.
    """

    with pytest.raises(ValueError):
        ExporterFactory.create(
            "unknown",
        )


def test_register_exporter() -> None:
    """
    Verify exporters can be registered.
    """

    class DummyExporter(BaseExporter):

        def metric_reader(self):
            return None

    ExporterFactory.register(
        "dummy",
        DummyExporter,
    )

    exporter = ExporterFactory.create(
        "dummy",
    )

    assert isinstance(
        exporter,
        DummyExporter,
    )