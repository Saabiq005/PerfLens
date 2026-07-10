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