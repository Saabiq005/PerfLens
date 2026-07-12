"""
Unit tests for MetricGenerator.
"""

from src.models.metric import Metric
from src.simulation.metric_generator import MetricGenerator


def test_generate_metric_returns_float() -> None:

    generator = MetricGenerator()

    metric = Metric(
        metric_id="latency",
        baseline=100,
        variance=10,
        distribution="normal",
        trend="stable",
    )

    value = generator.generate(metric)

    assert isinstance(value, float)


def test_zero_variance_returns_baseline() -> None:

    generator = MetricGenerator()

    metric = Metric(
        metric_id="latency",
        baseline=100,
        variance=0,
        distribution="normal",
        trend="stable",
    )

    assert generator.generate(metric) == 100.0


def test_generated_value_non_negative() -> None:

    generator = MetricGenerator()

    metric = Metric(
        metric_id="latency",
        baseline=20,
        variance=50,
        distribution="normal",
        trend="stable",
    )

    assert generator.generate(metric) >= 0