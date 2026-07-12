"""
Unit tests for the runtime Service model.
"""

import pytest
from src.config.exceptions import ConfigurationValidationError
from src.models.service import Service


def test_create_service() -> None:
    """Verify clean instantiation of the Service model."""
    service = Service(
        service_id="order_service",
        display_name="Order Service",
        description="Processes micro telemetry",
        domain="Orders",
        environment="development",
        deployment_tag="release-1",
        version="1.0.0",
        telemetry_enabled=True,
        telemetry_metrics=["latency", "throughput"],
        supported_scenarios=["healthy", "recovery"],
        initial_scenario="healthy",
    )

    assert service.service_id == "order_service"
    assert service.telemetry_enabled is True


def test_empty_id_raises() -> None:
    """Verify that an empty service ID triggers a ConfigurationValidationError at instantiation."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Service(
            service_id="",
            display_name="Order Service",
            description="Processes micro telemetry",
            domain="Orders",
            environment="development",
            deployment_tag="release-1",
            version="1.0.0",
            telemetry_enabled=True,
            telemetry_metrics=["latency"],
            supported_scenarios=["healthy"],
            initial_scenario="healthy",
        )
    assert "Service identifier cannot be empty" in str(excinfo.value)


def test_empty_display_name_raises() -> None:
    """Verify that an empty display name triggers an exception at instantiation."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Service(
            service_id="order_service",
            display_name="",
            description="Processes micro telemetry",
            domain="Orders",
            environment="development",
            deployment_tag="release-1",
            version="1.0.0",
            telemetry_enabled=True,
            telemetry_metrics=["latency"],
            supported_scenarios=["healthy"],
            initial_scenario="healthy",
        )
    assert "Display name cannot be empty" in str(excinfo.value)


def test_empty_metrics_raises() -> None:
    """Verify that an empty telemetry metrics list is rejected."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Service(
            service_id="order_service",
            display_name="Order Service",
            description="Processes micro telemetry",
            domain="Orders",
            environment="development",
            deployment_tag="release-1",
            version="1.0.0",
            telemetry_enabled=True,
            telemetry_metrics=[],
            supported_scenarios=["healthy"],
            initial_scenario="healthy",
        )
    assert "At least one telemetry metric is required" in str(excinfo.value)


def test_invalid_initial_scenario() -> None:
    """Verify that an initial scenario missing from supported scenarios causes an exception."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Service(
            service_id="order_service",
            display_name="Order Service",
            description="Processes micro telemetry",
            domain="Orders",
            environment="development",
            deployment_tag="release-1",
            version="1.0.0",
            telemetry_enabled=True,
            telemetry_metrics=["latency"],
            supported_scenarios=["healthy"],
            initial_scenario="error_storm",
        )
    assert "must exist in supported scenarios" in str(excinfo.value)


def test_capability_discovery_methods() -> None:
    """Verify metric publishing and scenario support verification rules."""
    service = Service(
        service_id="order_service",
        display_name="Order Service",
        description="Processes micro telemetry",
        domain="Orders",
        environment="development",
        deployment_tag="release-1",
        version="1.0.0",
        telemetry_enabled=True,
        telemetry_metrics=["latency"],
        supported_scenarios=["healthy"],
        initial_scenario="healthy",
    )

    assert service.supports_scenario("healthy") is True
    assert service.supports_scenario("error_storm") is False
    assert service.publishes_metric("latency") is True
    assert service.publishes_metric("throughput") is False


def test_to_dict() -> None:
    """Verify complete dictionary serialization behavior for downstream processing fields."""
    service = Service(
        service_id="order_service",
        display_name="Order Service",
        description="Processes micro telemetry",
        domain="Orders",
        environment="development",
        deployment_tag="release-1",
        version="1.0.0",
        telemetry_enabled=True,
        telemetry_metrics=["latency"],
        supported_scenarios=["healthy"],
        initial_scenario="healthy",
        owner="Platform Engineering",
    )

    data = service.to_dict()
    assert data["service_id"] == "order_service"
    assert data["owner"] == "Platform Engineering"