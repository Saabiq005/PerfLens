"""
Runtime service model for the PerfLens simulation engine.

Purpose:
    Represents a strongly typed simulated microservice profile context.

Responsibilities:
    - Store service architectural metadata and deployment info.
    - Maintain active telemetry configurations.
    - Provide utility interfaces for scenario capability discovery.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from src.config.exceptions import ConfigurationValidationError


@dataclass(slots=True, frozen=True)
class Service:
    """
    Immutable runtime representation of a simulated microservice.
    """

    service_id: str
    display_name: str
    description: str
    domain: str
    environment: str
    deployment_tag: str
    version: str
    telemetry_enabled: bool
    telemetry_metrics: list[str] = field(default_factory=list)
    supported_scenarios: list[str] = field(default_factory=list)
    initial_scenario: str = ""
    owner: str = ""
    criticality: str = ""
    sla: str = ""
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Perform strict runtime state validation using the framework exception hierarchy.
        """
        if not self.service_id.strip():
            raise ConfigurationValidationError("Service identifier cannot be empty.")

        if not self.display_name.strip():
            raise ConfigurationValidationError("Display name cannot be empty.")

        if not self.telemetry_metrics:
            raise ConfigurationValidationError("At least one telemetry metric is required.")

        if not self.supported_scenarios:
            raise ConfigurationValidationError("At least one supported scenario is required.")

        if self.initial_scenario not in self.supported_scenarios:
            raise ConfigurationValidationError(
                f"Initial scenario '{self.initial_scenario}' must exist in "
                f"supported scenarios for service '{self.service_id}'."
            )

    @classmethod
    def from_yaml_dict(cls, raw_data: dict[str, any]) -> Service:
        """
        Factory method to instantiate a Service domain model directly from 
        loaded configuration registry dictionary structures.
        """
        inner = raw_data.get("service", {})
        identity = inner.get("identity", {})
        deployment = inner.get("deployment", {})
        telemetry = inner.get("telemetry", {})
        scenarios = inner.get("scenarios", {})
        metadata = inner.get("metadata", {})

        return cls(
            service_id=identity.get("id"),
            display_name=identity.get("display_name"),
            description=identity.get("description"),
            domain=identity.get("domain"),
            environment=deployment.get("environment"),
            deployment_tag=deployment.get("deployment_tag"),
            version=deployment.get("version"),
            telemetry_enabled=telemetry.get("enabled", True),
            telemetry_metrics=telemetry.get("metrics", []),
            supported_scenarios=scenarios.get("supported", []),
            initial_scenario=scenarios.get("initial", ""),
            owner=metadata.get("owner", ""),
            criticality=metadata.get("criticality", ""),
            sla=metadata.get("sla", ""),
            tags=metadata.get("tags", [])
        )

    def supports_scenario(self, scenario_id: str) -> bool:
        """
        Determine whether the service supports a given scenario.
        """
        return scenario_id in self.supported_scenarios

    def publishes_metric(self, metric_id: str) -> bool:
        """
        Determine whether the service publishes a given metric.
        """
        return metric_id in self.telemetry_metrics

    def to_dict(self) -> dict[str, any]:
        """
        Convert the service model state into a standard dictionary.
        """
        return asdict(self)