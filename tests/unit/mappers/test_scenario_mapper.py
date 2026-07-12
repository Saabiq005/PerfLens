"""
Unit tests for ScenarioMapper.
"""

from src.mappers.scenario_mapper import ScenarioMapper
from src.models.metric import Metric
from src.models.scenario import Scenario


def test_map_scenario_configuration() -> None:

    configuration = {
        "scenario": {
            "schema_version": "1.0.0",
            "identity": {
                "id": "healthy",
                "display_name": "Healthy Operation",
                "description": "Healthy system.",
            },
            "runtime": {
                "duration": {
                    "minimum_seconds": 60,
                    "maximum_seconds": 180,
                }
            },
            "metrics": [
                {
                    "metric_id": "latency",
                    "baseline": 100,
                    "variance": 10,
                    "distribution": "normal",
                    "trend": "stable",
                },
                {
                    "metric_id": "throughput",
                    "baseline": 250,
                    "variance": 15,
                    "distribution": "normal",
                    "trend": "stable",
                },
            ],
            "transitions": {
                "traffic_spike": 0.70,
                "database_bottleneck": 0.20,
                "error_storm": 0.10,
            },
        }
    }

    scenario = ScenarioMapper.from_configuration(
        configuration,
    )

    assert isinstance(
        scenario,
        Scenario,
    )

    assert scenario.scenario_id == "healthy"

    assert scenario.display_name == "Healthy Operation"

    assert scenario.minimum_duration_seconds == 60

    assert scenario.maximum_duration_seconds == 180

    assert scenario.metric_count == 2

    assert scenario.transition_count == 3

    assert scenario.has_metric("latency")

    assert scenario.has_metric("throughput")

    latency = scenario.metric("latency")

    assert isinstance(
        latency,
        Metric,
    )

    assert latency.baseline == 100.0

    assert latency.variance == 10.0

    assert scenario.transitions["traffic_spike"] == 0.70