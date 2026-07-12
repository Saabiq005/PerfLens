"""
Mapper for converting metric configuration into runtime models.

Purpose:
    Convert validated metric configuration dictionaries into
    Metric domain models.

Responsibilities:
    - Translate configuration dictionaries.
    - Construct Metric objects.

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

from src.models.metric import Metric


# ============================================================================
# Classes
# ============================================================================


class MetricMapper:
    """
    Mapper for Metric runtime models.
    """

    @staticmethod
    def from_configuration(
        configuration: Mapping[str, Any],
    ) -> Metric:
        """
        Convert a validated metric configuration into a Metric model.

        Args:
            configuration:
                Metric configuration dictionary from a scenario.

        Returns:
            Runtime Metric instance.
        """
        return Metric(
            metric_id=configuration["metric_id"],
            baseline=float(configuration["baseline"]),
            variance=float(configuration["variance"]),
            distribution=configuration["distribution"],
            trend=configuration["trend"],
        )