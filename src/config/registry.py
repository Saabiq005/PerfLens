"""
Configuration registry for the PerfLens project.

Purpose:
    Centralizes access to all loaded configuration data.

Responsibilities:
    - Load configuration files.
    - Store configuration in memory.
    - Provide read-only access to configuration.

This module does NOT:
    - Validate configuration.
    - Modify configuration.
    - Perform business logic.
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
from src.config.loader import ConfigurationLoader

# ============================================================================
# Classes
# ============================================================================


class ConfigurationRegistry:
    """
    Registry containing all loaded PerfLens configuration.
    """

    def __init__(
        self,
        loader: ConfigurationLoader,
    ) -> None:
        """
        Initialize the configuration registry.

        Args:
            loader:
                Configuration loader instance.
        """
        self._loader = loader

        self._metric_catalog: dict[str, Any] = {}

        self._services: dict[str, dict[str, Any]] = {}

        self._scenarios: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        """
        Load all supported configuration.
        """
        self._metric_catalog = self._loader.load_file(
            ConfigCategory.METRICS,
            "metric_catalog.yaml",
        )

        self._services = self._loader.load_directory(
            ConfigCategory.SERVICES,
        )

        self._scenarios = self._loader.load_directory(
            ConfigCategory.SCENARIOS,
        )

    @property
    def metric_catalog(self) -> dict[str, Any]:
        """
        Return the metric catalog.
        """
        return self._metric_catalog

    @property
    def services(self) -> dict[str, dict[str, Any]]:
        """
        Return loaded services.
        """
        return self._services

    @property
    def scenarios(self) -> dict[str, dict[str, Any]]:
        """
        Return loaded scenarios.
        """
        return self._scenarios

    def get_service(
        self,
        service_name: str,
    ) -> dict[str, Any]:
        """
        Return a service configuration.

        Args:
            service_name:
                Service name.

        Returns:
            Service configuration.

        Raises:
            KeyError:
                If the service does not exist.
        """
        return self._services[service_name]

    def get_scenario(
        self,
        scenario_name: str,
    ) -> dict[str, Any]:
        """
        Return a scenario configuration.

        Args:
            scenario_name:
                Scenario name.

        Returns:
            Scenario configuration.

        Raises:
            KeyError:
                If the scenario does not exist.
        """
        return self._scenarios[scenario_name]

    def metric_exists(
        self,
        metric_id: str,
    ) -> bool:
        """
        Determine whether a metric exists.

        Args:
            metric_id:
                Metric identifier.

        Returns:
            True if the metric exists.
        """
        metrics = self._metric_catalog["catalog"]["metrics"]

        return any(
            metric["metric_id"] == metric_id
            for metric in metrics
        )

    def service_exists(
        self,
        service_name: str,
    ) -> bool:
        """
        Determine whether a service exists.
        """
        return service_name in self._services

    def scenario_exists(
        self,
        scenario_name: str,
    ) -> bool:
        """
        Determine whether a scenario exists.
        """
        return scenario_name in self._scenarios