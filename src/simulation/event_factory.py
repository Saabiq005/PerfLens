"""
Telemetry event factory for the PerfLens simulator.

Purpose:
    Construct TelemetryEvent objects from runtime models.

Responsibilities:
    - Create telemetry events.
    - Populate generated metric values.
    - Encapsulate event construction.

This module does NOT:
    - Manage scenarios.
    - Publish telemetry.
    - Persist data.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================

from src.models.scenario import Scenario
from src.models.service import Service
from src.models.telemetry import TelemetryEvent
from src.simulation.metric_generator import MetricGenerator


class EventFactory:
    """
    Factory responsible for constructing telemetry events.
    """

    def __init__(
        self,
        metric_generator: MetricGenerator | None = None,
    ) -> None:
        """
        Initialize the event factory.

        Args:
            metric_generator:
                Metric generator implementation.
        """
        self._metric_generator = (
            metric_generator
            if metric_generator is not None
            else MetricGenerator()
        )

    def create(
        self,
        service: Service,
        scenario: Scenario,
    ) -> TelemetryEvent:
        """
        Create a telemetry event.

        Args:
            service:
                Runtime service.

            scenario:
                Runtime scenario.

        Returns:
            Fully populated telemetry event.
        """

        event = TelemetryEvent(
            service_id=service.service_id,
            scenario_id=scenario.scenario_id,
        )

        for metric in scenario.metrics.values():

            value = self._metric_generator.generate(
                metric,
            )

            event.add_metric(
                metric.metric_id,
                value,
            )

        return event