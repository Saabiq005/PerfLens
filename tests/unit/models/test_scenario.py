"""
Unit tests for the runtime Scenario model.
"""

import pytest

from src.config.exceptions import ConfigurationValidationError
from src.models.metric import Metric
from src.models.scenario import Scenario


@pytest.fixture
def latency_metric() -> Metric:
    """Fixture providing a standard active latency metric instance."""
    return Metric(
        metric_id="latency",
        baseline=100.0,
        variance=10.0,
        distribution="normal",
        trend="stable",
    )


# ============================================================================
# Success Path Tests
# ============================================================================

def test_create_scenario_success(latency_metric: Metric) -> None:
    """Verify clean instantiation and property state of a valid Scenario."""
    scenario = Scenario(
        scenario_id="healthy",
        display_name="Healthy Operation",
        description="Normal application baseline status.",
        minimum_duration_seconds=60,
        maximum_duration_seconds=180,
        metrics={"latency": latency_metric},
        transitions={"traffic_spike": 1.0},
    )

    assert scenario.scenario_id == "healthy"
    assert scenario.display_name == "Healthy Operation"
    assert scenario.description == "Normal application baseline status."
    assert scenario.duration_range == (60, 180)
    assert scenario.metric_count == 1
    assert scenario.transition_count == 1


# ============================================================================
# Identity Validation Tests
# ============================================================================

def test_empty_scenario_id_raises(latency_metric: Metric) -> None:
    """Verify empty scenario_id throws ConfigurationValidationError."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="   ",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Scenario identifier cannot be empty" in str(excinfo.value)


def test_empty_display_name_raises(latency_metric: Metric) -> None:
    """Verify empty display_name throws ConfigurationValidationError."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Scenario display name cannot be empty" in str(excinfo.value)


def test_empty_description_raises(latency_metric: Metric) -> None:
    """Verify empty description throws ConfigurationValidationError."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="  ",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Scenario description cannot be empty" in str(excinfo.value)


# ============================================================================
# Duration Validation Tests
# ============================================================================

def test_negative_minimum_duration_raises(latency_metric: Metric) -> None:
    """Verify negative minimum duration throws an exception."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=-10,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Minimum duration cannot be negative" in str(excinfo.value)


def test_negative_maximum_duration_raises(latency_metric: Metric) -> None:
    """Verify negative maximum duration throws an exception."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=-5,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Maximum duration cannot be negative" in str(excinfo.value)


def test_minimum_duration_exceeds_maximum_raises(latency_metric: Metric) -> None:
    """Verify minimum duration exceeding maximum duration triggers validation error."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=200,
            maximum_duration_seconds=100,
            metrics={"latency": latency_metric},
            transitions={},
        )
    assert "Minimum duration cannot exceed maximum duration" in str(excinfo.value)


# ============================================================================
# Metric Mapping Validation Tests
# ============================================================================

def test_empty_metrics_raises() -> None:
    """Verify empty metric dictionary throws an exception."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={},
            transitions={},
        )
    assert "Scenario must contain at least one metric" in str(excinfo.value)


def test_mismatched_metric_key_raises(latency_metric: Metric) -> None:
    """Verify that mapping a metric under an incorrect dictionary key triggers an error."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"mismatched_key": latency_metric},
            transitions={},
        )
    assert "does not match metric identifier" in str(excinfo.value)


# ============================================================================
# Transition Validation Tests
# ============================================================================

def test_empty_transition_target_id_raises(latency_metric: Metric) -> None:
    """Verify that an empty space key inside transition states triggers an error."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={" ": 1.0},
        )
    assert "Transition scenario identifier cannot be empty" in str(excinfo.value)


def test_negative_transition_probability_raises(latency_metric: Metric) -> None:
    """Verify negative weights inside state transition rules are blocked."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={"traffic_spike": -0.2, "recovery": 1.2},
        )
    assert "Transition probability cannot be negative" in str(excinfo.value)


def test_invalid_transition_sum_raises(latency_metric: Metric) -> None:
    """Verify transition rules that do not sum to 1.0 fail validation."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Scenario(
            scenario_id="healthy",
            display_name="Healthy",
            description="Description",
            minimum_duration_seconds=60,
            maximum_duration_seconds=180,
            metrics={"latency": latency_metric},
            transitions={"traffic_spike": 0.5, "database_bottleneck": 0.1},
        )
    assert "Transition probabilities must sum to 1.0" in str(excinfo.value)


# ============================================================================
# Utility Helper & Accessor Tests
# ============================================================================

def test_metric_lookup_and_discovery(latency_metric: Metric) -> None:
    """Verify operational access methods perform correctly."""
    scenario = Scenario(
        scenario_id="healthy",
        display_name="Healthy",
        description="Description",
        minimum_duration_seconds=60,
        maximum_duration_seconds=180,
        metrics={"latency": latency_metric},
        transitions={"traffic_spike": 1.0},
    )

    assert scenario.has_metric("latency") is True
    assert scenario.has_metric("throughput") is False
    assert scenario.metric("latency") == latency_metric

    with pytest.raises(KeyError):
        scenario.metric("unknown")


def test_to_dict_serialization(latency_metric: Metric) -> None:
    """Verify complete dictionary parsing structure matches specifications."""
    scenario = Scenario(
        scenario_id="healthy",
        display_name="Healthy",
        description="Description",
        minimum_duration_seconds=60,
        maximum_duration_seconds=180,
        metrics={"latency": latency_metric},
        transitions={"traffic_spike": 1.0},
    )

    data = scenario.to_dict()
    assert data["scenario_id"] == "healthy"
    assert isinstance(data["metrics"], dict)
    assert data["metrics"]["latency"]["baseline"] == 100.0