"""
Telemetry exporter factory.

Purpose:
    Create telemetry exporter implementations.

Responsibilities:
    - Register exporter implementations.
    - Create exporters by name.

This module does NOT:
    - Configure MeterProvider.
    - Export metrics.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================

from src.telemetry.exporters.base import BaseExporter
from src.telemetry.exporters.console import ConsoleExporter


class ExporterFactory:
    """
    Factory for telemetry exporters.
    """

    _EXPORTERS: dict[str, type[BaseExporter]] = {
        "console": ConsoleExporter,  "otlp": OTLPExporter,
    }   

    # =======================================================================

    @classmethod
    def register(
        cls,
        name: str,
        exporter: type[BaseExporter],
    ) -> None:
        """
        Register a telemetry exporter.

        Args:
            name:
                Exporter identifier.

            exporter:
                Exporter implementation.
        """

        cls._EXPORTERS[name.lower()] = exporter

    # =======================================================================

    @classmethod
    def create(
        cls,
        name: str,
        **kwargs,
    ) -> BaseExporter:
        """
        Create a telemetry exporter.

        Args:
            name:
                Exporter name.

        Returns:
            Configured exporter.

        Raises:
            ValueError:
                If exporter is unsupported.
        """

        exporter = cls._EXPORTERS.get(
            name.lower(),
        )

        if exporter is None:

            supported = ", ".join(
                sorted(cls._EXPORTERS),
            )

            raise ValueError(
                f"Unsupported exporter '{name}'. "
                f"Supported exporters: {supported}"
            )

        return exporter(**kwargs)

    # =======================================================================

    @classmethod
    def supported_exporters(
        cls,
    ) -> tuple[str, ...]:
        """
        Return supported exporters.
        """

        return tuple(
            sorted(cls._EXPORTERS),
        )