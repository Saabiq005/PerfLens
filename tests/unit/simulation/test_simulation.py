"""
Unit tests for the PerfLens simulator.
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import Mock
from unittest.mock import patch

from src.models.service import Service
from src.models.telemetry import TelemetryEvent
from src.simulation.simulator import Simulator


# ============================================================================
# Fixtures
# ============================================================================


def create_service() -> Service:
    """
    Create a runtime service for testing.
    """
    return Service(
        service_id="inventory_service",
        display_name="Inventory Service",
        description="Inventory Service",
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
        sla="99.95%",
        tags=("inventory",),
    )


def create_event() -> TelemetryEvent:
    """
    Create a telemetry event for testing.
    """
    event = TelemetryEvent(
        service_id="inventory_service",
        scenario_id="healthy",
    )

    event.add_metric(
        "latency",
        100.5,
    )

    return event


# ============================================================================
# Tests
# ============================================================================


@patch("src.simulation.simulator.ScenarioEngine")
def test_simulator_initialization(
    mock_scenario_engine,
) -> None:
    """
    Verify simulator initializes correctly.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    simulator = Simulator(
        runtime_registry=runtime_registry,
        service_id="inventory_service",
    )

    assert simulator is not None

    runtime_registry.service.assert_called_once_with(
        "inventory_service",
    )


@patch("src.simulation.simulator.ScenarioEngine")
def test_next_event_returns_telemetry_event(
    mock_scenario_engine,
) -> None:
    """
    Verify next_event returns a TelemetryEvent.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    scenario = Mock()

    mock_scenario_engine.return_value.next.return_value = scenario

    event_factory = Mock()

    event = create_event()

    event_factory.create.return_value = event

    simulator = Simulator(
        runtime_registry=runtime_registry,
        service_id="inventory_service",
        event_factory=event_factory,
    )

    generated = simulator.next_event()

    assert generated is event

    event_factory.create.assert_called_once_with(
        service=create_service(),
        scenario=scenario,
    )


@patch("src.simulation.simulator.ScenarioEngine")
def test_next_event_contains_metrics(
    mock_scenario_engine,
) -> None:
    """
    Verify generated event contains metrics.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    mock_scenario_engine.return_value.next.return_value = Mock()

    event = create_event()

    event_factory = Mock()

    event_factory.create.return_value = event

    simulator = Simulator(
        runtime_registry,
        "inventory_service",
        event_factory,
    )

    generated = simulator.next_event()

    assert generated.metric_count == 1

    assert generated.has_metric(
        "latency",
    )


@patch("src.simulation.simulator.ScenarioEngine")
def test_run_returns_iterator(
    mock_scenario_engine,
) -> None:
    """
    Verify run returns an iterator.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    mock_scenario_engine.return_value.next.return_value = Mock()

    event_factory = Mock()

    event_factory.create.return_value = create_event()

    simulator = Simulator(
        runtime_registry,
        "inventory_service",
        event_factory,
    )

    iterator = simulator.run()

    assert isinstance(
        iterator,
        Iterator,
    )


@patch("src.simulation.simulator.ScenarioEngine")
def test_run_generates_multiple_events(
    mock_scenario_engine,
) -> None:
    """
    Verify run generates multiple events.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    mock_scenario_engine.return_value.next.return_value = Mock()

    event_factory = Mock()

    event_factory.create.return_value = create_event()

    simulator = Simulator(
        runtime_registry,
        "inventory_service",
        event_factory,
    )

    iterator = simulator.run()

    event_one = next(iterator)

    event_two = next(iterator)

    assert isinstance(
        event_one,
        TelemetryEvent,
    )

    assert isinstance(
        event_two,
        TelemetryEvent,
    )


@patch("src.simulation.simulator.ScenarioEngine")
def test_next_event_invokes_scenario_engine(
    mock_scenario_engine,
) -> None:
    """
    Verify ScenarioEngine.next() is invoked.
    """

    runtime_registry = Mock()

    runtime_registry.service.return_value = create_service()

    scenario = Mock()

    engine = mock_scenario_engine.return_value

    engine.next.return_value = scenario

    event_factory = Mock()

    event_factory.create.return_value = create_event()

    simulator = Simulator(
        runtime_registry,
        "inventory_service",
        event_factory,
    )

    simulator.next_event()

    engine.next.assert_called_once()


@patch("src.simulation.simulator.ScenarioEngine")
def test_next_event_invokes_event_factory(
    mock_scenario_engine,
) -> None:
    """
    Verify EventFactory.create() is invoked.
    """

    runtime_registry = Mock()

    service = create_service()

    runtime_registry.service.return_value = service

    scenario = Mock()

    mock_scenario_engine.return_value.next.return_value = scenario

    event_factory = Mock()

    event_factory.create.return_value = create_event()

    simulator = Simulator(
        runtime_registry,
        "inventory_service",
        event_factory,
    )

    simulator.next_event()

    event_factory.create.assert_called_once_with(
        service=service,
        scenario=scenario,
    )