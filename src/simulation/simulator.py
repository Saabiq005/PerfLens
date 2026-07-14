"""
Core simulator for the PerfLens simulation engine.

Purpose:
    Coordinate runtime components to generate telemetry events.

Responsibilities:
    - Manage simulation lifecycle.
    - Produce telemetry events.
    - Coordinate runtime services.

This module does NOT:
    - Publish telemetry.
    - Persist data.
    - Manage configuration loading.
"""

from __future__ import annotations
import time
from collections.abc import Iterator

from src.mappers.runtime_registry import RuntimeRegistry
from src.models.service import Service
from src.models.telemetry import TelemetryEvent
from src.simulation.event_factory import EventFactory
from src.simulation.scenario_engine import ScenarioEngine


class Simulator:
    """
    Runtime telemetry simulator.
    """

    def __init__(
        self,
        runtime_registry: RuntimeRegistry,
        service_id: str,
        event_factory: EventFactory | None = None,
    ) -> None:
        """
        Initialize the simulator.
        """

        self._runtime_registry = runtime_registry

        self._service: Service = runtime_registry.service(
            service_id,
        )

        self._event_factory = (
            event_factory
            if event_factory is not None
            else EventFactory()
        )

        self._scenario_engine = ScenarioEngine(
            service=self._service,
            runtime_registry=runtime_registry,
        )

    # ===================================================================

    def next_event(
        self,
    ) -> TelemetryEvent:
        """
        Generate a single telemetry event.
        """

        scenario = self._scenario_engine.next()

        return self._event_factory.create(
            service=self._service,
            scenario=scenario,
        )

    # ===================================================================

    def run(
        self,
    ) -> Iterator[TelemetryEvent]:
        """
        Generate telemetry events indefinitely.
        """

        while True:

            yield self.next_event()

            time.sleep(5)