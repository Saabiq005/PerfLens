"""
Unit tests for MetricMapper.
"""

from src.mappers.metric_mapper import MetricMapper
from src.models.metric import Metric


def test_map_metric_configuration() -> None:

    configuration = {
        "metric_id": "latency",
        "baseline": 100,
        "variance": 10,
        "distribution": "normal",
        "trend": "stable",
    }

    metric = MetricMapper.from_configuration(
        configuration,
    )

    assert isinstance(metric, Metric)

    assert metric.metric_id == "latency"

    assert metric.baseline == 100.0

    assert metric.variance == 10.0

    assert metric.distribution == "normal"

    assert metric.trend == "stable"