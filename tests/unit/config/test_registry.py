from pathlib import Path

from src.config.loader import ConfigurationLoader
from src.config.registry import ConfigurationRegistry


def test_registry_loads_metric_catalog() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert registry.metric_catalog


def test_registry_loads_services() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert len(registry.services) == 2


def test_registry_loads_scenarios() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert len(registry.scenarios) == 5


def test_metric_exists() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert registry.metric_exists("latency")


def test_metric_not_exists() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert not registry.metric_exists("invalid")


def test_service_exists() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert registry.service_exists("order_service")


def test_scenario_exists() -> None:

    loader = ConfigurationLoader(Path("configs"))

    registry = ConfigurationRegistry(loader)

    registry.load()

    assert registry.scenario_exists("healthy")