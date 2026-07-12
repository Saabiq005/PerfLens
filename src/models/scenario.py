"""
Runtime scenario model for the PerfLens simulation engine.

Purpose:
    Represents a runtime simulation scenario.

Responsibilities:
    - Store scenario information.
    - Store runtime duration.
    - Store runtime metrics.
    - Store transition probabilities.
    - Validate model state.
    - Support serialization.

This model does NOT:
    - Load YAML configuration.
    - Perform scenario transitions.
    - Generate telemetry.
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
from src.models.metric import Metric


# ============================================================================
# Classes
# ============================================================================


@dataclass(slots=True, frozen=True)
class Scenario:
    """
    Runtime representation of a simulation scenario.
    """

    scenario_id: str

    display_name: str

    description: str

    minimum_duration_seconds: int

    maximum_duration_seconds: int

    metrics: dict[str, Metric]

    transitions: dict[str, float]

    def __post_init__(self) -> None:
        """
        Validate the scenario after initialization.
        """
        self._validate_identity()

        self._validate_duration()

        self._validate_metrics()

        self._validate_transitions()

    # =======================================================================
    # Validation
    # =======================================================================

    def _validate_identity(self) -> None:
        """
        Validate scenario identity.
        """
        if not self.scenario_id.strip():
            raise ConfigurationValidationError(
                message="Scenario identifier cannot be empty.",
            )

        if not self.display_name.strip():
            raise ConfigurationValidationError(
                message="Scenario display name cannot be empty.",
            )

        if not self.description.strip():
            raise ConfigurationValidationError(
                message="Scenario description cannot be empty.",
            )

    def _validate_duration(self) -> None:
        """
        Validate runtime duration.
        """
        if self.minimum_duration_seconds < 0:
            raise ConfigurationValidationError(
                message="Minimum duration cannot be negative.",
            )

        if self.maximum_duration_seconds < 0:
            raise ConfigurationValidationError(
                message="Maximum duration cannot be negative.",
            )

        if (
            self.minimum_duration_seconds
            > self.maximum_duration_seconds
        ):
            raise ConfigurationValidationError(
                message=(
                    "Minimum duration cannot exceed "
                    "maximum duration."
                ),
            )

    def _validate_metrics(self) -> None:
        """
        Validate runtime metrics.
        """
        if not self.metrics:
            raise ConfigurationValidationError(
                message="Scenario must contain at least one metric.",
            )

        for metric_id, metric in self.metrics.items():

            if metric.metric_id != metric_id:
                raise ConfigurationValidationError(
                    message=(
                        f"Metric key '{metric_id}' does not "
                        f"match metric identifier "
                        f"'{metric.metric_id}'."
                    ),
                )

    def _validate_transitions(self) -> None:
        """
        Validate transition probabilities.
        """
        if not self.transitions:
            return

        total_probability = 0.0

        for scenario_id, probability in self.transitions.items():

            if not scenario_id.strip():
                raise ConfigurationValidationError(
                    message=(
                        "Transition scenario identifier "
                        "cannot be empty."
                    ),
                )

            if probability < 0:
                raise ConfigurationValidationError(
                    message=(
                        "Transition probability cannot "
                        "be negative."
                    ),
                )

            total_probability += probability

        if abs(total_probability - 1.0) > 1e-6:
            raise ConfigurationValidationError(
                message=(
                    "Transition probabilities must "
                    "sum to 1.0."
                ),
            )

    # =======================================================================
    # Helper Methods
    # =======================================================================

    def metric(
        self,
        metric_id: str,
    ) -> Metric:
        """
        Return a metric by identifier.

        Args:
            metric_id:
                Metric identifier.

        Returns:
            Runtime metric.

        Raises:
            KeyError:
                If the metric does not exist.
        """
        return self.metrics[metric_id]

    def has_metric(
        self,
        metric_id: str,
    ) -> bool:
        """
        Determine whether the scenario contains a metric.
        """
        return metric_id in self.metrics

    @property
    def duration_range(self) -> tuple[int, int]:
        """
        Return the runtime duration range.

        Returns:
            Tuple containing the minimum and maximum duration.
        """
        return (
            self.minimum_duration_seconds,
            self.maximum_duration_seconds,
        )

    @property
    def metric_count(self) -> int:
        """
        Return the number of runtime metrics.
        """
        return len(self.metrics)

    @property
    def transition_count(self) -> int:
        """
        Return the number of possible transitions.
        """
        return len(self.transitions)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the scenario to a dictionary.

        Returns:
            Dictionary representation of the scenario.
        """
        return asdict(self)