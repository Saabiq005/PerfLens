"""
OpenTelemetry metric recorder.

Purpose:
    Record generated metric values using OpenTelemetry.

Responsibilities:
    - Build OpenTelemetry attributes.
    - Retrieve instruments.
    - Record metric values.

This module does NOT:
    - Generate metrics.
    - Configure MeterProvider.
    - Manage simulation.
"""

from __future__ import annotations

from opentelemetry.metrics import Counter
from opentelemetry.metrics import Histogram
from opentelemetry.metrics import UpDownCounter

from src.models.metric import Metric
from src.models.scenario import Scenario
from src.models.service import Service
from src.telemetry.instrument_registry import InstrumentRegistry


class MetricRecorder:
    """
    Records runtime metrics using OpenTelemetry.
    """

    def __init__(
        self,
        registry: InstrumentRegistry,
    ) -> None:

        self._registry = registry

    # ===============================================================

    def record(
        self,
        service: Service,
        scenario: Scenario,
        metric: Metric,
        value: float,
    ) -> None:
        """
        Record a metric value.
        """

        instrument = self._registry.instrument(
            metric,
        )

        attributes = self._attributes(
            service,
            scenario,
        )

        if isinstance(
            instrument,
            Histogram,
        ):

            instrument.record(
                value,
                attributes=attributes,
            )

            return

        if isinstance(
            instrument,
            Counter,
        ):

            instrument.add(
                max(
                    value,
                    0.0,
                ),
                attributes=attributes,
            )

            return

        if isinstance(
            instrument,
            UpDownCounter,
        ):

            instrument.add(
                value,
                attributes=attributes,
            )

            return

    # ===============================================================

    @staticmethod
    def _attributes(
        service: Service,
        scenario: Scenario,
    ) -> dict[str, str]:
        """
        Build OpenTelemetry attributes.
        """

        return {

            "service.id": service.service_id,

            "service.name": service.display_name,

            "service.version": service.version,

            "deployment.environment": service.environment,

            "scenario.id": scenario.scenario_id,

            "scenario.name": scenario.display_name,

            "scenario.description": scenario.description,
        }