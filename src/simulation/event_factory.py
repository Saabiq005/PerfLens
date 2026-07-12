"""
Telemetry event factory for the PerfLens simulator.

Purpose:
    Construct TelemetryEvent objects from runtime models.

Responsibilities:
    - Create telemetry events.
    - Generate metric values.
    - Record metrics using OpenTelemetry.
    - Encapsulate event construction.

This module does NOT:
    - Manage scenarios.
    - Configure OpenTelemetry.
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
from src.telemetry.metric_recorder import MetricRecorder


# ============================================================================
# Classes
# ============================================================================


class EventFactory:
    """
    Factory responsible for constructing telemetry events.
    """

    def __init__(
        self,
        metric_generator: MetricGenerator | None = None,
        metric_recorder: MetricRecorder | None = None,
    ) -> None:
        """
        Initialize the event factory.

        Args:
            metric_generator:
                Runtime metric generator.

            metric_recorder:
                OpenTelemetry metric recorder.
                If None, metrics are not recorded through OpenTelemetry.
        """

        self._metric_generator = (
            metric_generator
            if metric_generator is not None
            else MetricGenerator()
        )

        self._metric_recorder = metric_recorder

    # =======================================================================

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

            # --------------------------------------------------------------
            # Generate synthetic metric value
            # --------------------------------------------------------------

            value = self._metric_generator.generate(
                metric,
            )

            # --------------------------------------------------------------
            # Preserve existing TelemetryEvent behaviour
            # --------------------------------------------------------------

            event.add_metric(
                metric.metric_id,
                value,
            )

            # --------------------------------------------------------------
            # Record the metric using OpenTelemetry
            # --------------------------------------------------------------

            if self._metric_recorder is not None:

                self._metric_recorder.record(
                    service=service,
                    scenario=scenario,
                    metric=metric,
                    value=value,
                )

        return event