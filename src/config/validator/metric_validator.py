"""
Metric catalog validator for the PerfLens project.

Purpose:
    Validates the structure and contents of the metric catalog.

Responsibilities:
    - Validate catalog metadata.
    - Validate metric definitions.
    - Validate aggregation configuration.
    - Validate validation configuration.
    - Detect duplicate metric identifiers.

This module does NOT:
    - Load configuration.
    - Validate cross references.
    - Create domain objects.
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


class MetricValidator(BaseValidator):
    """
    Validator for the PerfLens metric catalog.
    """

    REQUIRED_CATALOG_FIELDS = [
        "name",
        "version",
        "schema_version",
        "description",
        "author",
        "last_updated",
        "metrics",
    ]

    REQUIRED_METRIC_FIELDS = [
        "metric_id",
        "display_name",
        "description",
        "category",
        "unit",
        "data_type",
        "precision",
        "aggregation",
        "validation",
        "enabled",
        "tags",
    ]

    REQUIRED_AGGREGATION_FIELDS = [
        "default",
        "supported",
    ]

    REQUIRED_VALIDATION_FIELDS = [
        "minimum",
        "maximum",
        "nullable",
    ]

    def validate(
        self,
        configuration: Mapping[str, Any],
    ) -> None:
        """
        Validate the complete metric catalog.
        """
        catalog = self._require_field(
            configuration,
            "catalog",
        )

        self._require_type(
            catalog,
            dict,
            "catalog",
        )

        self._validate_catalog(catalog)

    # ===================================================================
    # Catalog Validation
    # ===================================================================

    def _validate_catalog(
        self,
        catalog: Mapping[str, Any],
    ) -> None:
        """
        Validate catalog metadata.
        """
        self._require_fields(
            catalog,
            self.REQUIRED_CATALOG_FIELDS,
        )

        self._require_non_empty(
            catalog["name"],
            "name",
        )

        self._require_non_empty(
            catalog["version"],
            "version",
        )

        self._require_non_empty(
            catalog["schema_version"],
            "schema_version",
        )

        self._require_non_empty(
            catalog["author"],
            "author",
        )

        metrics = catalog["metrics"]

        self._require_type(
            metrics,
            list,
            "metrics",
        )

        self._validate_metrics(metrics)

    # ===================================================================
    # Metric Validation
    # ===================================================================

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

            self._require_unique(
                metric["metric_id"],
                metric_ids,
                "metric_id",
            )

    def _validate_metric(
        self,
        metric: Mapping[str, Any],
    ) -> None:
        """
        Validate a single metric definition.
        """
        self._require_fields(
            metric,
            self.REQUIRED_METRIC_FIELDS,
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
            metric["display_name"],
            str,
            "display_name",
        )

        self._require_type(
            metric["description"],
            str,
            "description",
        )

        self._require_type(
            metric["category"],
            str,
            "category",
        )

        self._require_type(
            metric["unit"],
            str,
            "unit",
        )

        self._require_type(
            metric["data_type"],
            str,
            "data_type",
        )

        self._require_type(
            metric["precision"],
            int,
            "precision",
        )

        self._require_positive_number(
            metric["precision"],
            "precision",
        )

        self._require_type(
            metric["enabled"],
            bool,
            "enabled",
        )

        self._require_type(
            metric["tags"],
            list,
            "tags",
        )

        self._require_non_empty(
            metric["tags"],
            "tags",
        )

        self._validate_aggregation(
            metric["aggregation"],
        )

        self._validate_validation(
            metric["validation"],
        )

    # ===================================================================
    # Aggregation Validation
    # ===================================================================

    def _validate_aggregation(
        self,
        aggregation: Mapping[str, Any],
    ) -> None:
        """
        Validate aggregation configuration.
        """
        self._require_fields(
            aggregation,
            self.REQUIRED_AGGREGATION_FIELDS,
        )

        self._require_type(
            aggregation["default"],
            str,
            "aggregation.default",
        )

        self._require_type(
            aggregation["supported"],
            list,
            "aggregation.supported",
        )

        self._require_non_empty(
            aggregation["supported"],
            "aggregation.supported",
        )

        if aggregation["default"] not in aggregation["supported"]:
            self._raise_validation_error(
                "Default aggregation must exist in supported aggregations."
            )

    # ===================================================================
    # Validation Block Validation
    # ===================================================================

    def _validate_validation(
        self,
        validation: Mapping[str, Any],
    ) -> None:
        """
        Validate metric validation block.
        """
        self._require_fields(
            validation,
            self.REQUIRED_VALIDATION_FIELDS,
        )

        self._require_type(
            validation["minimum"],
            (int, float),
            "validation.minimum",
        )

        self._require_type(
            validation["maximum"],
            (int, float),
            "validation.maximum",
        )

        self._require_type(
            validation["nullable"],
            bool,
            "validation.nullable",
        )

        if validation["minimum"] > validation["maximum"]:
            self._raise_validation_error(
                "Validation minimum cannot exceed validation maximum."
            )