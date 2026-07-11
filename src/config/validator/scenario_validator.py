"""
Scenario configuration validator for the PerfLens project.

Purpose:
    Validates the structure and contents of scenario configurations.

Responsibilities:
    - Validate scenario metadata.
    - Validate runtime configuration.
    - Validate metric behavior.
    - Validate transition probabilities.

This module does NOT:
    - Validate metric references.
    - Load configuration files.
    - Create simulation objects.
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

from src.config.validator.base_validator import BaseValidator


# ============================================================================
# Classes
# ============================================================================


class ScenarioValidator(BaseValidator):
    """
    Validator for scenario configuration.
    """

    REQUIRED_SCENARIO_FIELDS = [
        "schema_version",
        "identity",
        "runtime",
        "metrics",
        "transitions",
    ]

    REQUIRED_IDENTITY_FIELDS = [
        "id",
        "display_name",
        "description",
    ]

    REQUIRED_RUNTIME_FIELDS = [
        "duration",
    ]

    REQUIRED_DURATION_FIELDS = [
        "minimum_seconds",
        "maximum_seconds",
    ]

    REQUIRED_METRIC_FIELDS = [
        "metric_id",
        "baseline",
        "variance",
        "distribution",
        "trend",
    ]

    def validate(
        self,
        configuration: Mapping[str, Any],
    ) -> None:
        """
        Validate an entire scenario configuration.
        """
        scenario = self._require_field(
            configuration,
            "scenario",
        )

        self._require_type(
            scenario,
            dict,
            "scenario",
        )

        self._validate_scenario(
            scenario,
        )

    # ===================================================================
    # Scenario
    # ===================================================================

    def _validate_scenario(
        self,
        scenario: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            scenario,
            self.REQUIRED_SCENARIO_FIELDS,
        )

        self._validate_identity(
            scenario["identity"],
        )

        self._validate_runtime(
            scenario["runtime"],
        )

        self._validate_metrics(
            scenario["metrics"],
        )

        self._validate_transitions(
            scenario["transitions"],
        )

    # ===================================================================
    # Identity
    # ===================================================================

    def _validate_identity(
        self,
        identity: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            identity,
            self.REQUIRED_IDENTITY_FIELDS,
        )

        for field in self.REQUIRED_IDENTITY_FIELDS:

            self._require_type(
                identity[field],
                str,
                field,
            )

            self._require_non_empty(
                identity[field],
                field,
            )

    # ===================================================================
    # Runtime
    # ===================================================================

    def _validate_runtime(
        self,
        runtime: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            runtime,
            self.REQUIRED_RUNTIME_FIELDS,
        )

        duration = runtime["duration"]

        self._require_fields(
            duration,
            self.REQUIRED_DURATION_FIELDS,
        )

        self._require_type(
            duration["minimum_seconds"],
            int,
            "minimum_seconds",
        )

        self._require_type(
            duration["maximum_seconds"],
            int,
            "maximum_seconds",
        )

        self._require_positive_number(
            duration["minimum_seconds"],
            "minimum_seconds",
        )

        self._require_positive_number(
            duration["maximum_seconds"],
            "maximum_seconds",
        )

        if (
            duration["minimum_seconds"]
            > duration["maximum_seconds"]
        ):
            self._raise_validation_error(
                "minimum_seconds cannot exceed maximum_seconds."
            )

    # ===================================================================
    # Metrics
    # ===================================================================

    def _validate_metrics(
        self,
        metrics: list[dict[str, Any]],
    ) -> None:

        self._require_non_empty(
            metrics,
            "metrics",
        )

        metric_ids: set[str] = set()

        for metric in metrics:

            self._require_fields(
                metric,
                self.REQUIRED_METRIC_FIELDS,
            )

            self._require_unique(
                metric["metric_id"],
                metric_ids,
                "metric_id",
            )

            self._require_type(
                metric["metric_id"],
                str,
                "metric_id",
            )

            self._require_non_empty(
                metric["metric_id"],
                "metric_id",
            )

            self._require_type(
                metric["baseline"],
                (int, float),
                "baseline",
            )

            self._require_type(
                metric["variance"],
                (int, float),
                "variance",
            )

            self._require_positive_number(
                metric["variance"],
                "variance",
            )

            self._require_type(
                metric["distribution"],
                str,
                "distribution",
            )

            self._require_type(
                metric["trend"],
                str,
                "trend",
            )

    # ===================================================================
    # Transitions
    # ===================================================================

    def _validate_transitions(
        self,
        transitions: Mapping[str, float],
    ) -> None:

        self._require_non_empty(
            transitions,
            "transitions",
        )

        total_probability = 0.0

        for scenario, probability in transitions.items():

            self._require_type(
                scenario,
                str,
                "transition",
            )

            self._require_type(
                probability,
                (int, float),
                "transition_probability",
            )

            if probability < 0:
                self._raise_validation_error(
                    "Transition probabilities cannot be negative."
                )

            total_probability += probability

        if abs(total_probability - 1.0) > 0.000001:
            self._raise_validation_error(
                "Transition probabilities must sum to 1.0."
            )