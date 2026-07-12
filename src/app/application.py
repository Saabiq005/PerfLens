"""
PerfLens application.

Purpose:
    Compose and run the PerfLens application.

Responsibilities:
    - Load configuration.
    - Build runtime models.
    - Configure OpenTelemetry.
    - Construct the simulator.
    - Execute the simulation.

This module does NOT:
    - Generate telemetry.
    - Validate business rules.
    - Record metrics directly.
"""

from __future__ import annotations

from pathlib import Path

from src.common.enums import ConfigCategory
from src.config.loader import ConfigurationLoader
from src.config.registry import ConfigurationRegistry
from src.mappers.runtime_registry import RuntimeRegistry
from src.simulation.event_factory import EventFactory
from src.simulation.simulator import Simulator
from src.telemetry.instrument_registry import InstrumentRegistry
from src.telemetry.metric_recorder import MetricRecorder
from src.telemetry.provider import TelemetryProvider


class Application:
    """
    PerfLens application.
    """

    def __init__(
        self,
        configuration_directory: Path = Path("configs"),
    ) -> None:

        self._configuration_directory = configuration_directory

        self._runtime_registry: RuntimeRegistry | None = None

        self._simulator: Simulator | None = None

    # ======================================================================

    def initialize(
        self,
    ) -> None:
        """
        Initialize the application.
        """

        configuration_registry = self._build_configuration_registry()

        runtime_registry = RuntimeRegistry.from_configuration(
            configuration_registry,
        )

        telemetry_provider = TelemetryProvider()

        instrument_registry = InstrumentRegistry(
            telemetry_provider.meter,
        )

        metric_recorder = MetricRecorder(
            instrument_registry,
        )

        event_factory = EventFactory(
            metric_recorder=metric_recorder,
        )

        simulator = Simulator(
            runtime_registry=runtime_registry,
            service_id="inventory_service",
            event_factory=event_factory,
        )

        self._runtime_registry = runtime_registry

        self._simulator = simulator

    # ======================================================================

    def run(
        self,
    ) -> None:
        """
        Run the application.
        """

        if self._simulator is None:
            raise RuntimeError(
                "Application has not been initialized."
            )

        for event in self._simulator.run():

            # Temporary while TelemetryEvent still exists.
            print(
                event,
            )

    # ======================================================================

    def _build_configuration_registry(
        self,
    ) -> ConfigurationRegistry:
        """
        Load all configuration into the registry.
        """

        loader = ConfigurationLoader(
            self._configuration_directory,
        )

        registry = ConfigurationRegistry(
            loader,
        )

        # Adjust these calls to match your existing registry API.
        registry.load_category(
            ConfigCategory.METRICS,
        )

        registry.load_category(
            ConfigCategory.SCENARIOS,
        )

        registry.load_category(
            ConfigCategory.SERVICES,
        )

        return registry