"""
Service configuration validator for the PerfLens project.

Purpose:
    Validates the structure and contents of service configurations.

Responsibilities:
    - Validate service identity.
    - Validate deployment configuration.
    - Validate telemetry configuration.
    - Validate supported scenarios.
    - Validate metadata.

This module does NOT:
    - Validate metric references.
    - Validate scenario references.
    - Load configuration files.
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


class ServiceValidator(BaseValidator):
    """
    Validator for PerfLens service configuration.
    """

    REQUIRED_SERVICE_FIELDS = [
        "identity",
        "deployment",
        "telemetry",
        "scenarios",
        "metadata",
    ]

    REQUIRED_IDENTITY_FIELDS = [
        "id",
        "display_name",
        "description",
        "domain",
    ]

    REQUIRED_DEPLOYMENT_FIELDS = [
        "environment",
        "deployment_tag",
        "version",
    ]

    REQUIRED_TELEMETRY_FIELDS = [
        "enabled",
        "metrics",
    ]

    REQUIRED_SCENARIO_FIELDS = [
        "supported",
        "initial",
    ]

    REQUIRED_METADATA_FIELDS = [
        "owner",
        "criticality",
        "sla",
        "tags",
    ]

    def validate(
        self,
        configuration: Mapping[str, Any],
    ) -> None:
        """
        Validate an entire service configuration.
        """
        service = self._require_field(
            configuration,
            "service",
        )

        self._require_type(
            service,
            dict,
            "service",
        )

        self._validate_service(service)

    # ===================================================================
    # Service
    # ===================================================================

    def _validate_service(
        self,
        service: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            service,
            self.REQUIRED_SERVICE_FIELDS,
        )

        self._validate_identity(
            service["identity"],
        )

        self._validate_deployment(
            service["deployment"],
        )

        self._validate_telemetry(
            service["telemetry"],
        )

        self._validate_scenarios(
            service["scenarios"],
        )

        self._validate_metadata(
            service["metadata"],
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
    # Deployment
    # ===================================================================

    def _validate_deployment(
        self,
        deployment: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            deployment,
            self.REQUIRED_DEPLOYMENT_FIELDS,
        )

        for field in self.REQUIRED_DEPLOYMENT_FIELDS:

            self._require_type(
                deployment[field],
                str,
                field,
            )

            self._require_non_empty(
                deployment[field],
                field,
            )

    # ===================================================================
    # Telemetry
    # ===================================================================

    def _validate_telemetry(
        self,
        telemetry: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            telemetry,
            self.REQUIRED_TELEMETRY_FIELDS,
        )

        self._require_type(
            telemetry["enabled"],
            bool,
            "enabled",
        )

        metrics = telemetry["metrics"]

        self._require_type(
            metrics,
            list,
            "metrics",
        )

        self._require_non_empty(
            metrics,
            "metrics",
        )

        seen: set[str] = set()

        for metric in metrics:

            self._require_type(
                metric,
                str,
                "metric",
            )

            self._require_non_empty(
                metric,
                "metric",
            )

            self._require_unique(
                metric,
                seen,
                "metric",
            )

    # ===================================================================
    # Scenarios
    # ===================================================================

    def _validate_scenarios(
        self,
        scenarios: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            scenarios,
            self.REQUIRED_SCENARIO_FIELDS,
        )

        supported = scenarios["supported"]

        self._require_type(
            supported,
            list,
            "supported",
        )

        self._require_non_empty(
            supported,
            "supported",
        )

        seen: set[str] = set()

        for scenario in supported:

            self._require_type(
                scenario,
                str,
                "scenario",
            )

            self._require_non_empty(
                scenario,
                "scenario",
            )

            self._require_unique(
                scenario,
                seen,
                "scenario",
            )

        self._require_type(
            scenarios["initial"],
            str,
            "initial",
        )

        self._require_non_empty(
            scenarios["initial"],
            "initial",
        )

    # ===================================================================
    # Metadata
    # ===================================================================

    def _validate_metadata(
        self,
        metadata: Mapping[str, Any],
    ) -> None:

        self._require_fields(
            metadata,
            self.REQUIRED_METADATA_FIELDS,
        )

        self._require_type(
            metadata["owner"],
            str,
            "owner",
        )

        self._require_type(
            metadata["criticality"],
            str,
            "criticality",
        )

        self._require_type(
            metadata["sla"],
            str,
            "sla",
        )

        tags = metadata["tags"]

        self._require_type(
            tags,
            list,
            "tags",
        )

        self._require_non_empty(
            tags,
            "tags",
        )

        seen: set[str] = set()

        for tag in tags:

            self._require_type(
                tag,
                str,
                "tag",
            )

            self._require_non_empty(
                tag,
                "tag",
            )

            self._require_unique(
                tag,
                seen,
                "tag",
            )