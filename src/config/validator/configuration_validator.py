"""
Configuration validator for the PerfLens project.

Purpose:
    Coordinates validation of all PerfLens configuration.

Responsibilities:
    - Invoke all validators.
    - Validate complete configuration.

This module does NOT:
    - Load configuration.
    - Store configuration.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================

from src.common.enums import ConfigCategory
from src.config.registry import ConfigurationRegistry
from src.config.validator.metric_validator import MetricValidator
from src.config.validator.reference_validator import ReferenceValidator
from src.config.validator.scenario_validator import ScenarioValidator
from src.config.validator.service_validator import ServiceValidator


# ============================================================================
# Classes
# ============================================================================


class ConfigurationValidator:
    """
    Coordinates configuration validation.
    """

    def __init__(self) -> None:

        self._metric_validator = MetricValidator()

        self._scenario_validator = ScenarioValidator()

        self._service_validator = ServiceValidator()

        self._reference_validator = ReferenceValidator()

    def validate(
        self,
        registry: ConfigurationRegistry,
    ) -> None:
        """
        Validate all loaded configuration.
        """

        self._metric_validator.validate(
            registry.get(
                ConfigCategory.METRICS,
            )
        )

        scenarios = registry.get(
            ConfigCategory.SCENARIOS,
        )

        for scenario in scenarios.values():

            self._scenario_validator.validate(
                scenario,
            )

        services = registry.get(
            ConfigCategory.SERVICES,
        )

        for service in services.values():

            self._service_validator.validate(
                service,
            )

        self._reference_validator.validate(
            registry,
        )