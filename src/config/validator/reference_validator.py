"""
Cross-reference validator for the PerfLens configuration system.

Purpose:
    Validates relationships between configuration files.

Responsibilities:
    - Validate scenario metric references.
    - Validate service metric references.
    - Validate service scenario references.
    - Validate initial scenario references.

This module does NOT:
    - Validate configuration structure.
    - Load configuration files.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from typing import Any

# ============================================================================
# Local Imports
# ============================================================================

from src.common.enums import ConfigCategory
from src.config.registry import ConfigurationRegistry
from src.config.validator.base_validator import BaseValidator


# ============================================================================
# Classes
# ============================================================================


class ReferenceValidator(BaseValidator):
    """
    Validator for cross-configuration references.
    """

    def validate(
        self,
        registry: ConfigurationRegistry,
    ) -> None:
        """
        Validate all cross-file references.
        """
        self._validate_scenario_metrics(registry)
        self._validate_service_metrics(registry)
        self._validate_service_scenarios(registry)

    # =======================================================================
    # Scenario -> Metric
    # =======================================================================

    def _validate_scenario_metrics(
        self,
        registry: ConfigurationRegistry,
    ) -> None:

        scenarios = registry.get(
            ConfigCategory.SCENARIOS,
        )

        for scenario_name, configuration in scenarios.items():

            metrics = configuration["scenario"]["metrics"]

            for metric in metrics:

                metric_id = metric["metric_id"]

                if not registry.metric_exists(metric_id):

                    self._raise_validation_error(
                        f"Scenario '{scenario_name}' references "
                        f"unknown metric '{metric_id}'."
                    )

    # =======================================================================
    # Service -> Metric
    # =======================================================================

    def _validate_service_metrics(
        self,
        registry: ConfigurationRegistry,
    ) -> None:

        services = registry.get(
            ConfigCategory.SERVICES,
        )

        for service_name, configuration in services.items():

            metrics = (
                configuration["service"]
                ["telemetry"]
                ["metrics"]
            )

            for metric in metrics:

                if not registry.metric_exists(metric):

                    self._raise_validation_error(
                        f"Service '{service_name}' references "
                        f"unknown metric '{metric}'."
                    )

    # =======================================================================
    # Service -> Scenario
    # =======================================================================

    def _validate_service_scenarios(
        self,
        registry: ConfigurationRegistry,
    ) -> None:

        services = registry.get(
            ConfigCategory.SERVICES,
        )

        for service_name, configuration in services.items():

            scenario_config = (
                configuration["service"]
                ["scenarios"]
            )

            supported = scenario_config["supported"]

            initial = scenario_config["initial"]

            for scenario in supported:

                if not registry.scenario_exists(
                    scenario,
                ):
                    self._raise_validation_error(
                        f"Service '{service_name}' references "
                        f"unknown scenario '{scenario}'."
                    )

            if not registry.scenario_exists(initial):

                self._raise_validation_error(
                    f"Service '{service_name}' references "
                    f"unknown initial scenario '{initial}'."
                )

            if initial not in supported:

                self._raise_validation_error(
                    f"Initial scenario '{initial}' "
                    f"must exist in supported scenarios "
                    f"for service '{service_name}'."
                )