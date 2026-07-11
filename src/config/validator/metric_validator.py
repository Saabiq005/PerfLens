"""
Metric configuration validator for the PerfLens project.

Purpose:
    Validates the structure and content of the metric catalog.

Responsibilities:
    - Validate metric catalog structure.
    - Validate required fields.
    - Detect duplicate metric identifiers.
    - Validate basic data types.

This module does NOT:
    - Load configuration files.
    - Validate scenario references.
    - Create Metric objects.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from typing import Any

# ============================================================================
# Local Imports
# ============================================================================

from src.config.validator.base_validator import BaseValidator

# ============================================================================
# Classes
# ============================================================================


class MetricValidator(BaseValidator):
    """
    Validator for metric catalog configuration.
    """

    REQUIRED_FIELDS = (
        "metric_id",
        "display_name",
        "description",
        "category",
        "unit",
        "data_type",
        "aggregation",
    )

    def validate(
        self,
        data: dict[str, Any],
    ) -> None:
        """
        Validate the metric catalog.
        """
        catalog = self._require_field(data, "catalog")

        self._require_type(
            catalog,
            dict,
            "catalog",
        )

        metrics = self._require_field(
            catalog,
            "metrics",
        )

        self._require_type(
            metrics,
            list,
            "metrics",
        )

        self._validate_metrics(metrics)

    def _validate_metrics(
        self,
        metrics: list[dict[str, Any]],
    ) -> None:
        """
        Validate all metric definitions.
        """
        metric_ids: set[str] = set()

        for metric in metrics:

            self._validate_metric(metric)

            metric_id = metric["metric_id"]

            if metric_id in metric_ids:
                self._raise_validation_error(
                    f"Duplicate metric_id '{metric_id}'."
                )

            metric_ids.add(metric_id)

    def _validate_metric(
        self,
        metric: dict[str, Any],
    ) -> None:
        """
        Validate an individual metric.
        """
        self._require_fields(
            metric,
            list(self.REQUIRED_FIELDS),
        )

        for field in self.REQUIRED_FIELDS:

            value = metric[field]

            self._require_type(
                value,
                str,
                field,
            )

            self._require_non_empty(
                value,
                field,
            )