"""
Unit tests for the runtime Metric model.
"""

import pytest
from src.config.exceptions import ConfigurationValidationError
from src.models.metric import Metric  # Assumes saved in src/models/metric.py


def test_metric_instantiation_success() -> None:
    """Verify clean initialization and properties of a valid Metric instance."""
    metric = Metric(
        metric_id="latency",
        baseline=120.5,
        variance=30.0,
        distribution="normal",
        trend="stable"
    )
    assert metric.metric_id == "latency"
    assert metric.upper_bound == 150.5
    assert metric.lower_bound == 90.5


def test_metric_lower_bound_clipped_at_zero() -> None:
    """Verify that lower_bound property prevents negative limits and clips to zero."""
    metric = Metric(
        metric_id="error_rate",
        baseline=5.0,
        variance=15.0,
        distribution="normal",
        trend="increasing"
    )
    assert metric.lower_bound == 0.0


@pytest.mark.parametrize(
    "metric_id, baseline, variance, distribution, trend, error_msg",
    [
        ("   ", 100, 10, "normal", "stable", "Metric identifier cannot be empty"),
        ("latency", -10, 10, "normal", "stable", "Metric baseline cannot be negative"),
        ("latency", 100, -5, "normal", "stable", "Metric variance cannot be negative"),
        ("latency", 100, 10, "  ", "stable", "Distribution cannot be empty"),
        ("latency", 100, 10, "normal", "", "Trend cannot be empty"),
    ]
)
def test_metric_validation_failures(metric_id, baseline, variance, distribution, trend, error_msg) -> None:
    """Verify strict instantiation lifecycle validation rules throw framework errors."""
    with pytest.raises(ConfigurationValidationError) as excinfo:
        Metric(
            metric_id=metric_id,
            baseline=baseline,
            variance=variance,
            distribution=distribution,
            trend=trend
        )
    assert error_msg in str(excinfo.value)


def test_metric_serialization() -> None:
    """Verify dictionary mapping payload generation matches internal states."""
    metric = Metric(
        metric_id="throughput",
        baseline=250.0,
        variance=20.0,
        distribution="poisson",
        trend="stable"
    )
    data = metric.to_dict()
    assert data["metric_id"] == "throughput"
    assert data["baseline"] == 250.0