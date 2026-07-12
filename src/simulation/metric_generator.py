"""
Runtime metric generator for the PerfLens simulator.

Purpose:
    Generate synthetic values for runtime metrics.

Responsibilities:
    - Generate metric values.
    - Delegate statistical generation to DistributionEngine.
    - Apply runtime trends.

This module does NOT:
    - Generate telemetry events.
    - Manage scenarios.
    - Publish telemetry.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================

from src.models.metric import Metric
from src.simulation.distributions import DistributionEngine


class MetricGenerator:
    """
    Runtime metric generator.
    """

    def __init__(
        self,
        distribution_engine: type[DistributionEngine] = DistributionEngine,
    ) -> None:
        """
        Initialize the metric generator.

        Args:
            distribution_engine:
                Distribution engine implementation.
        """
        self._distribution_engine = distribution_engine

    def generate(
        self,
        metric: Metric,
    ) -> float:
        """
        Generate a synthetic metric value.

        Args:
            metric:
                Runtime metric.

        Returns:
            Generated metric value.
        """

        value = self._distribution_engine.generate(
            distribution=metric.distribution,
            baseline=metric.baseline,
            variance=metric.variance,
        )

        value = self._apply_trend(
            value,
            metric,
        )

        return round(
            value,
            4,
        )

    # =======================================================================

    def _apply_trend(
        self,
        value: float,
        metric: Metric,
    ) -> float:
        """
        Apply runtime trend.

        Currently only 'stable' is implemented.

        Future implementations may include:

        - increasing
        - decreasing
        - cyclical
        - seasonal
        - exponential
        """

        match metric.trend.lower():

            case "stable":
                return value

            case _:
                return value