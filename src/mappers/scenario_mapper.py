"""
Mapper for converting scenario configuration into runtime models.

Purpose:
    Convert validated scenario configuration dictionaries into
    Scenario domain models.

Responsibilities:
    - Translate scenario configuration.
    - Map runtime metrics.
    - Construct Scenario objects.

This module does NOT:
    - Load configuration.
    - Validate configuration.
    - Generate telemetry.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================

from src.mappers.metric_mapper import MetricMapper
from src.models.metric import Metric
from src.models.scenario import Scenario


# ============================================================================
# Classes
# ============================================================================


class ScenarioMapper:
    """
    Mapper for Scenario runtime models.
    """

    @staticmethod
    def from_configuration(
        configuration: Mapping[str, Any],
    ) -> Scenario:
        """
        Convert a validated scenario configuration into a Scenario model.

        Args:
            configuration:
                Complete scenario configuration dictionary.

        Returns:
            Runtime Scenario instance.
        """
        scenario = configuration["scenario"]

        identity = scenario["identity"]

        duration = scenario["runtime"]["duration"]

        metrics = ScenarioMapper._map_metrics(
            scenario["metrics"],
        )

        transitions = dict(
            scenario["transitions"],
        )

        return Scenario(
            scenario_id=identity["id"],
            display_name=identity["display_name"],
            description=identity["description"],
            minimum_duration_seconds=duration["minimum_seconds"],
            maximum_duration_seconds=duration["maximum_seconds"],
            metrics=metrics,
            transitions=transitions,
        )

    # =======================================================================
    # Private Helpers
    # =======================================================================

    @staticmethod
    def _map_metrics(
        metric_configurations: list[Mapping[str, Any]],
    ) -> dict[str, Metric]:
        """
        Convert scenario metric configurations into runtime Metric objects.

        Args:
            metric_configurations:
                Metric configuration list.

        Returns:
            Dictionary of Metric objects keyed by metric identifier.
        """
        metrics: dict[str, Metric] = {}

        for configuration in metric_configurations:

            metric = MetricMapper.from_configuration(
                configuration,
            )

            metrics[metric.metric_id] = metric

        return metrics