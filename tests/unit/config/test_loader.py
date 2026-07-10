"""
Unit tests for ConfigurationLoader.
"""

from pathlib import Path

import pytest

from src.common.enums import ConfigCategory
from src.config.exceptions import (
    ConfigurationNotFoundError,
    UnsupportedConfigurationError,
)
from src.config.loader import ConfigurationLoader

from src.config.exceptions import (
    ConfigurationNotFoundError,
    UnsupportedConfigurationError,  
)
from enum import Enum 

def test_resolve_existing_metric_catalog() -> None:
    """Verify an existing configuration file is resolved."""

    loader = ConfigurationLoader(Path("configs"))

    path = loader.resolve_path(
        ConfigCategory.METRICS,
        "metric_catalog.yaml",
    )

    assert path.exists()
    assert path.name == "metric_catalog.yaml"


def test_resolve_missing_file() -> None:
    """Verify a missing configuration file raises an exception."""

    loader = ConfigurationLoader(Path("configs"))

    with pytest.raises(ConfigurationNotFoundError):
        loader.resolve_path(
            ConfigCategory.METRICS,
            "missing.yaml",
        )


def test_resolve_invalid_extension() -> None:
    """Verify unsupported file extensions are rejected."""

    loader = ConfigurationLoader(Path("configs"))

    with pytest.raises(UnsupportedConfigurationError):
        loader.resolve_path(
            ConfigCategory.METRICS,
            "metric_catalog.json",
        )


def test_resolve_returns_absolute_path() -> None:
    """Verify the returned path is absolute."""

    loader = ConfigurationLoader(Path("configs"))

    path = loader.resolve_path(
        ConfigCategory.METRICS,
        "metric_catalog.yaml",
    )

    assert path.is_absolute()

def test_exists_returns_true() -> None:
    """Verify an existing configuration returns True."""

    loader = ConfigurationLoader(Path("configs"))

    assert loader.exists(
        ConfigCategory.METRICS,
        "metric_catalog.yaml",
    )


def test_exists_returns_false_for_missing_file() -> None:
    """Verify a missing configuration returns False."""

    loader = ConfigurationLoader(Path("configs"))

    assert not loader.exists(
        ConfigCategory.METRICS,
        "missing.yaml",
    )


def test_exists_returns_false_for_invalid_extension() -> None:
    """Verify unsupported extensions return False."""

    loader = ConfigurationLoader(Path("configs"))

    assert not loader.exists(
        ConfigCategory.METRICS,
        "metric_catalog.json",
    )

def test_list_metric_files() -> None:
    """Verify metric configuration files are discovered."""

    loader = ConfigurationLoader(Path("configs"))

    files = loader.list_files(ConfigCategory.METRICS)

    assert len(files) == 1
    assert files[0].name == "metric_catalog.yaml"


def test_list_scenario_files() -> None:
    """Verify all scenario configuration files are returned."""

    loader = ConfigurationLoader(Path("configs"))

    files = loader.list_files(ConfigCategory.SCENARIOS)

    assert len(files) == 5


def test_list_files_returns_sorted_paths() -> None:
    """Verify configuration files are returned in sorted order."""

    loader = ConfigurationLoader(Path("configs"))

    files = loader.list_files(ConfigCategory.SCENARIOS)

    names = [file.name for file in files]

    assert names == sorted(names)


def test_list_missing_category_directory() -> None:
    """Verify missing category directories raise an exception."""

    loader = ConfigurationLoader(Path("configs"))

    # Use an existing enum temporarily pointed at a directory you know
    # does not exist for this test setup, or create a temporary directory
    # structure in a future fixture-based test.

    # This test will be improved once we introduce pytest fixtures.


def test_load_metric_catalog() -> None:
    """Verify a valid YAML configuration is loaded."""

    loader = ConfigurationLoader(Path("configs"))

    config = loader.load_file(
        ConfigCategory.METRICS,
        "metric_catalog.yaml",
    )

    assert isinstance(config, dict)
    assert "catalog" in config


def test_load_scenario_configuration() -> None:
    """Verify a scenario configuration loads successfully."""

    loader = ConfigurationLoader(Path("configs"))

    config = loader.load_file(
        ConfigCategory.SCENARIOS,
        "healthy.yaml",
    )

    assert "scenario" in config


def test_load_missing_configuration() -> None:
    """Verify loading a missing file raises an exception."""

    loader = ConfigurationLoader(Path("configs"))

    with pytest.raises(ConfigurationNotFoundError):
        loader.load_file(
            ConfigCategory.METRICS,
            "missing.yaml",
        )