"""
Mapper for converting service configuration into runtime models.

Purpose:
    Convert validated service configuration dictionaries into
    Service domain models.

Responsibilities:
    - Translate service configuration.
    - Construct Service objects.

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

from src.models.service import Service


# ============================================================================
# Classes
# ============================================================================


class ServiceMapper:
    """
    Mapper for Service runtime models.
    """

    @staticmethod
    def from_configuration(
        configuration: Mapping[str, Any],
    ) -> Service:
        """
        Convert a validated service configuration into a Service model.

        Args:
            configuration:
                Complete service configuration.

        Returns:
            Runtime Service instance.
        """
        service = configuration["service"]

        identity = service["identity"]

        deployment = service["deployment"]

        telemetry = service["telemetry"]

        scenarios = service["scenarios"]

        metadata = service["metadata"]

        return Service(
            service_id=identity["id"],
            display_name=identity["display_name"],
            description=identity["description"],
            domain=identity["domain"],
            environment=deployment["environment"],
            deployment_tag=deployment["deployment_tag"],
            version=deployment["version"],
            telemetry_enabled=telemetry["enabled"],
            telemetry_metrics=tuple(
                telemetry["metrics"],
            ),
            supported_scenarios=tuple(
                scenarios["supported"],
            ),
            initial_scenario=scenarios["initial"],
            owner=metadata["owner"],
            criticality=metadata["criticality"],
            sla=metadata["sla"],
            tags=tuple(
                metadata["tags"],
            ),
        )