"""
Unit tests for the PerfLens configuration registry.

Purpose:
    Verify the behavior of the ConfigurationRegistry.

Responsibilities:
    - Verify configuration loading.
    - Verify configuration retrieval.
    - Verify existence checks.
    - Verify registry state.

This module does NOT:
    - Validate configuration contents.
    - Test YAML parsing.
    - Test business validation.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from pathlib import Path

# ============================================================================
# Third-Party Imports
# ============================================================================

import pytest

# ============================================================================
# Local Imports
# ============================================================================

from src.common.enums import ConfigCategory
from src.config.loader import ConfigurationLoader
from src.config.registry import ConfigurationRegistry


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def registry() -> ConfigurationRegistry:
    """
    Create a fully loaded configuration registry.
    """
    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    return registry


# ============================================================================
# Initialization Tests
# ============================================================================


def test_registry_initializes_empty() -> None:
    """
    Verify a newly created registry is empty.
    """
    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    assert not registry.contains(ConfigCategory.METRICS)
    assert not registry.contains(ConfigCategory.SERVICES)
    assert not registry.contains(ConfigCategory.SCENARIOS)


# ============================================================================
# Loading Tests
# ============================================================================


def test_registry_loads_metric_catalog(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify metric catalog is loaded.
    """
    metrics = registry.get(ConfigCategory.METRICS)

    assert isinstance(metrics, dict)

    assert "catalog" in metrics


def test_registry_loads_services(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify service configurations are loaded.
    """
    services = registry.get(ConfigCategory.SERVICES)

    assert isinstance(services, dict)

    assert len(services) == 2


def test_registry_loads_scenarios(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify scenario configurations are loaded.
    """
    scenarios = registry.get(ConfigCategory.SCENARIOS)

    assert isinstance(scenarios, dict)

    assert len(scenarios) == 5


# ============================================================================
# Contains Tests
# ============================================================================


def test_contains_metrics(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify metric category is present.
    """
    assert registry.contains(ConfigCategory.METRICS)


def test_contains_services(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify service category is present.
    """
    assert registry.contains(ConfigCategory.SERVICES)


def test_contains_scenarios(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify scenario category is present.
    """
    assert registry.contains(ConfigCategory.SCENARIOS)


# ============================================================================
# Get Tests
# ============================================================================


def test_get_metric_catalog(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify metric catalog retrieval.
    """
    catalog = registry.get(
        ConfigCategory.METRICS,
    )

    assert "catalog" in catalog


def test_get_services(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify service retrieval.
    """
    services = registry.get(
        ConfigCategory.SERVICES,
    )

    assert "order_service" in services

    assert "inventory_service" in services


def test_get_scenarios(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify scenario retrieval.
    """
    scenarios = registry.get(
        ConfigCategory.SCENARIOS,
    )

    assert "healthy" in scenarios

    assert "traffic_spike" in scenarios

    assert "database_bottleneck" in scenarios

    assert "error_storm" in scenarios

    assert "recovery" in scenarios


def test_get_unloaded_category_raises_key_error() -> None:
    """
    Verify accessing unloaded categories raises KeyError.
    """
    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    with pytest.raises(KeyError):
        registry.get(
            ConfigCategory.METRICS,
        )


# ============================================================================
# Metric Tests
# ============================================================================


def test_metric_exists_latency(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify latency metric exists.
    """
    assert registry.metric_exists("latency")


def test_metric_exists_throughput(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify throughput metric exists.
    """
    assert registry.metric_exists("throughput")


def test_metric_exists_error_rate(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify error_rate metric exists.
    """
    assert registry.metric_exists("error_rate")


def test_metric_exists_trace_duration(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify trace_duration metric exists.
    """
    assert registry.metric_exists("trace_duration")


def test_metric_not_exists(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify invalid metric returns False.
    """
    assert not registry.metric_exists(
        "cpu_usage"
    )


# ============================================================================
# Service Tests
# ============================================================================


def test_service_exists_order(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify order service exists.
    """
    assert registry.service_exists(
        "order_service"
    )


def test_service_exists_inventory(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify inventory service exists.
    """
    assert registry.service_exists(
        "inventory_service"
    )


def test_service_not_exists(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify invalid service returns False.
    """
    assert not registry.service_exists(
        "payment_service"
    )


# ============================================================================
# Scenario Tests
# ============================================================================


def test_scenario_exists_healthy(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify healthy scenario exists.
    """
    assert registry.scenario_exists(
        "healthy"
    )


def test_scenario_exists_traffic_spike(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify traffic spike scenario exists.
    """
    assert registry.scenario_exists(
        "traffic_spike"
    )


def test_scenario_exists_database_bottleneck(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify database bottleneck scenario exists.
    """
    assert registry.scenario_exists(
        "database_bottleneck"
    )


def test_scenario_exists_error_storm(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify error storm scenario exists.
    """
    assert registry.scenario_exists(
        "error_storm"
    )


def test_scenario_exists_recovery(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify recovery scenario exists.
    """
    assert registry.scenario_exists(
        "recovery"
    )


def test_scenario_not_exists(
    registry: ConfigurationRegistry,
) -> None:
    """
    Verify invalid scenario returns False.
    """
    assert not registry.scenario_exists(
        "stress_test"
    )