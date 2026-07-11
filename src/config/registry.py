"""
Configuration registry for the PerfLens project.

Purpose:
    Centralizes access to all loaded configuration data.

Responsibilities:
    - Load all configuration categories.
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
        self._registry: dict[ConfigCategory, Any] = {}

    def load(self) -> None:
        """
        Load all supported configuration.
        """
        self._registry[ConfigCategory.METRICS] = (
            self._loader.load_file(
                ConfigCategory.METRICS,
                "metric_catalog.yaml",
            )
        )

        self._registry[ConfigCategory.SERVICES] = (
            self._loader.load_directory(
                ConfigCategory.SERVICES,
            )
        )

        self._registry[ConfigCategory.SCENARIOS] = (
            self._loader.load_directory(
                ConfigCategory.SCENARIOS,
            )
        )

    def get(
        self,
        category: ConfigCategory,
    ) -> Any:
        """
        Return configuration for a category.

        Args:
            category:
                Configuration category.

        Returns:
            Loaded configuration.

        Raises:
            KeyError:
                If the category has not been loaded.
        """
        return self._registry[category]

    def contains(
        self,
        category: ConfigCategory,
    ) -> bool:
        """
        Determine whether a category has been loaded.
        """
        return category in self._registry

    def metric_exists(
        self,
        metric_id: str,
    ) -> bool:
        """
        Determine whether a metric exists.
        """
        catalog = self.get(ConfigCategory.METRICS)

        metrics = catalog["catalog"]["metrics"]

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
        services = self.get(
            ConfigCategory.SERVICES,
        )

        return service_name in services

    def scenario_exists(
        self,
        scenario_name: str,
    ) -> bool:
        """
        Determine whether a scenario exists.
        """
        scenarios = self.get(
            ConfigCategory.SCENARIOS,
        )

        return scenario_name in scenarios