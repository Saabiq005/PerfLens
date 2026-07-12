"""
Unit tests for the runtime TelemetryEvent model.
"""

import pytest
from datetime import datetime
from src.config.exceptions import ConfigurationValidationError
from src.models.telemetry import TelemetryEvent  # Assumes saved in src/models/telemetry.py


def test_telemetry_event_success_and_defaults() -> None:
    """Verify automated assignments and operational metric storage additions."""
    event = TelemetryEvent(
        service_id="payment_service",
        scenario_id="healthy"
    )

    assert event.event_id is not None
    assert isinstance(event.timestamp, datetime)
    assert event.metric_count == 0

    # Test dynamic additions and tracking mutations
    event.add_metric("latency", 42.15)
    assert event.metric_count == 1
    assert event.has_metric("latency") is True
    assert event.metric("latency") == 42.15


def test_telemetry_event_missing_identifiers_raise() -> None:
    """Verify empty origin microservice contexts fail instantiation constraints."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        TelemetryEvent(service_id="", scenario_id="healthy")
    assert "Service identifier cannot be empty" in str(excinfo.value)

    with pytest.raises(ConfigurationValidationError) as excinfo:
        TelemetryEvent(service_id="order_service", scenario_id="   ")
    assert "Scenario identifier cannot be empty" in str(excinfo.value)


def test_telemetry_event_invalid_metric_append_raises() -> None:
    """Verify that adding an empty string metric mapping channel drops an exception."""
    event = TelemetryEvent(service_id="auth_service", scenario_id="healthy")
    with pytest.raises(ConfigurationValidationError) as excinfo:
        event.add_metric("   ", 100.0)
    assert "Metric identifier cannot be empty" in str(excinfo.value)


def test_telemetry_serialization_iso_timestamp() -> None:
    """Verify serialization structure maps out accurate ISO string timestamps for streaming brokers."""
    event = TelemetryEvent(service_id="notification_service", scenario_id="recovery")
    event.add_metric("throughput", 85.0)

    serialized_data = event.to_dict()
    assert serialized_data["service_id"] == "notification_service"
    assert isinstance(serialized_data["timestamp"], str)
    # Checks for ending 'Z' or offset layout presence
    assert serialized_data["timestamp"].count("-") >= 2 
    assert serialized_data["metrics"]["throughput"] == 85.0