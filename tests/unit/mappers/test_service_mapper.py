"""
Unit tests for ServiceMapper.
"""

from src.mappers.service_mapper import ServiceMapper
from src.models.service import Service


def test_map_service_configuration() -> None:

    configuration = {
        "service": {
            "identity": {
                "id": "inventory_service",
                "display_name": "Inventory Service",
                "description": "Inventory",
                "domain": "Inventory Management",
            },
            "deployment": {
                "environment": "development",
                "deployment_tag": "release-1",
                "version": "1.0.0",
            },
            "telemetry": {
                "enabled": True,
                "metrics": [
                    "latency",
                    "throughput",
                    "error_rate",
                    "trace_duration",
                ],
            },
            "scenarios": {
                "supported": [
                    "healthy",
                    "traffic_spike",
                    "database_bottleneck",
                ],
                "initial": "healthy",
            },
            "metadata": {
                "owner": "Platform Engineering",
                "criticality": "high",
                "sla": "99.95%",
                "tags": [
                    "inventory",
                    "warehouse",
                    "api",
                ],
            },
        }
    }

    service = ServiceMapper.from_configuration(
        configuration,
    )

    assert isinstance(
        service,
        Service,
    )

    assert service.service_id == "inventory_service"

    assert service.display_name == "Inventory Service"

    assert service.environment == "development"

    assert service.telemetry_enabled

    assert service.supports_scenario(
        "healthy",
    )

    assert service.publishes_metric(
        "latency",
    )

    assert not service.publishes_metric(
        "cpu",
    )