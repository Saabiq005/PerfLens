"""
Runtime metric model for the PerfLens simulation engine.

Purpose:
    Represents the runtime behaviour of a telemetry metric
    within a simulation scenario.

Responsibilities:
    - Store runtime metric configuration.
    - Validate model state.
    - Support serialization.

This model does NOT:
    - Load YAML configuration.
    - Generate metric values.
    - Perform statistical calculations.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================

from src.config.exceptions import ConfigurationValidationError


# ============================================================================
# Classes
# ============================================================================


@dataclass(slots=True, frozen=True)
class Metric:
    """
    Runtime representation of a telemetry metric.

    Attributes:
        metric_id:
            Unique metric identifier.

        baseline:
            Expected baseline value.

        variance:
            Maximum deviation from the baseline.

        distribution:
            Statistical distribution used when generating
            synthetic values.

        trend:
            Runtime trend applied during simulation.
    """

    metric_id: str

    baseline: float

    variance: float

    distribution: str

    trend: str

    def __post_init__(self) -> None:
        """
        Validate the metric after initialization.

        Raises:
            ConfigurationValidationError:
                If the metric contains invalid values.
        """
        self._validate_metric_id()
        self._validate_baseline()
        self._validate_variance()
        self._validate_distribution()
        self._validate_trend()

    # =======================================================================
    # Validation
    # =======================================================================

    def _validate_metric_id(self) -> None:
        """
        Validate the metric identifier.
        """
        if not self.metric_id.strip():
            raise ConfigurationValidationError(
                message="Metric identifier cannot be empty.",
            )

    def _validate_baseline(self) -> None:
        """
        Validate the baseline value.
        """
        if self.baseline < 0:
            raise ConfigurationValidationError(
                message="Metric baseline cannot be negative.",
            )

    def _validate_variance(self) -> None:
        """
        Validate the variance value.
        """
        if self.variance < 0:
            raise ConfigurationValidationError(
                message="Metric variance cannot be negative.",
            )

    def _validate_distribution(self) -> None:
        """
        Validate the distribution.
        """
        if not self.distribution.strip():
            raise ConfigurationValidationError(
                message="Distribution cannot be empty.",
            )

    def _validate_trend(self) -> None:
        """
        Validate the trend.
        """
        if not self.trend.strip():
            raise ConfigurationValidationError(
                message="Trend cannot be empty.",
            )

    # =======================================================================
    # Utility Methods
    # =======================================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the metric to a dictionary.

        Returns:
            Dictionary representation of the metric.
        """
        return asdict(self)

    @property
    def upper_bound(self) -> float:
        """
        Return the maximum expected value.

        Returns:
            Baseline plus variance.
        """
        return self.baseline + self.variance

    @property
    def lower_bound(self) -> float:
        """
        Return the minimum expected value.

        Returns:
            Baseline minus variance.
        """
        return max(
            0.0,
            self.baseline - self.variance,
        )