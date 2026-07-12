"""
Base exporter interface for the PerfLens telemetry subsystem.

Purpose:
    Define the contract for telemetry exporters.

Responsibilities:
    - Create MetricReaders.
    - Hide exporter implementation details.

This module does NOT:
    - Configure MeterProvider.
    - Export metrics directly.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

# ============================================================================
# OpenTelemetry Imports
# ============================================================================

from opentelemetry.sdk.metrics.export import MetricReader


class BaseExporter(ABC):
    """
    Abstract base class for telemetry exporters.
    """

    @abstractmethod
    def metric_reader(
        self,
    ) -> MetricReader:
        """
        Return the configured MetricReader.

        Returns:
            Configured OpenTelemetry MetricReader.
        """
        raise NotImplementedError