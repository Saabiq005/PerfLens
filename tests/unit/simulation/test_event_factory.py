"""
Unit tests for EventFactory.
"""

from src.models.metric import Metric
from src.models.scenario import Scenario
from src.models.service import Service
from src.models.telemetry import TelemetryEvent
from src.simulation.event_factory import EventFactory


def test_create_event() -> None:

    metric = Metric(
        metric_id="latency",
        baseline=100,
        variance=10,
        distribution="normal",
        trend="stable",
    )

    scenario = Scenario(
        scenario_id="healthy",
        display_name="Healthy",
        description="Healthy scenario",
        minimum_duration_seconds=60,
        maximum_duration_seconds=120,
        metrics={
            "latency": metric,
        },
        transitions={
            "healthy": 1.0,
        },
    )

    service = Service(
        service_id="inventory_service",
        display_name="Inventory",
        description="Inventory service",
        domain="Inventory",
        environment="development",
        deployment_tag="release-1",
        version="1.0.0",
        telemetry_enabled=True,
        telemetry_metrics=("latency",),
        supported_scenarios=("healthy",),
        initial_scenario="healthy",
        owner="Platform",
        criticality="high",
        sla="99.9%",
        tags=("inventory",),
    )

    factory = EventFactory()

    event = factory.create(
        service,
        scenario,
    )

    assert isinstance(
        event,
        TelemetryEvent,
    )

    assert event.service_id == "inventory_service"

    assert event.scenario_id == "healthy"

    assert event.metric_count == 1

    assert event.has_metric("latency")