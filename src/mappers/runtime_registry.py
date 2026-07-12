"""
Runtime registry for the PerfLens simulation engine.

Purpose:
    Converts validated configuration dictionaries into runtime
    domain models and exposes them to the simulator.

Responsibilities:
    - Build runtime Scenario objects.
    - Build runtime Service objects.
    - Provide runtime lookup methods.

This module does NOT:
    - Load configuration files.
    - Validate configuration.
    - Generate telemetry.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass, field

# ============================================================================
# Local Imports
# ============================================================================

from src.common.enums import ConfigCategory
from src.config.registry import ConfigurationRegistry
from src.mappers.scenario_mapper import ScenarioMapper
from src.mappers.service_mapper import ServiceMapper
from src.models.scenario import Scenario
from src.models.service import Service


# ============================================================================
# Classes
# ============================================================================


@dataclass(slots=True)
class RuntimeRegistry:
    """
    Runtime object registry.
    """

    scenarios: dict[str, Scenario] = field(
        default_factory=dict
    )

    services: dict[str, Service] = field(
        default_factory=dict
    )

    @classmethod
    def from_configuration(
        cls,
        registry: ConfigurationRegistry,
    ) -> "RuntimeRegistry":
        """
        Build a runtime registry from validated configuration.
        """

        runtime = cls()

        runtime._load_scenarios(
            registry,
        )

        runtime._load_services(
            registry,
        )

        return runtime

    # ===================================================================

    def _load_scenarios(
        self,
        registry: ConfigurationRegistry,
    ) -> None:

        configurations = registry.get(
            ConfigCategory.SCENARIOS,
        )

        for configuration in configurations.values():

            scenario = ScenarioMapper.from_configuration(
                configuration,
            )

            self.scenarios[
                scenario.scenario_id
            ] = scenario

    # ===================================================================

    def _load_services(
        self,
        registry: ConfigurationRegistry,
    ) -> None:

        configurations = registry.get(
            ConfigCategory.SERVICES,
        )

        for configuration in configurations.values():

            service = ServiceMapper.from_configuration(
                configuration,
            )

            self.services[
                service.service_id
            ] = service

    # ===================================================================
    # Lookup Helpers
    # ===================================================================

    def scenario(
        self,
        scenario_id: str,
    ) -> Scenario:

        return self.scenarios[
            scenario_id
        ]

    def service(
        self,
        service_id: str,
    ) -> Service:

        return self.services[
            service_id
        ]

    def has_scenario(
        self,
        scenario_id: str,
    ) -> bool:

        return scenario_id in self.scenarios

    def has_service(
        self,
        service_id: str,
    ) -> bool:

        return service_id in self.services