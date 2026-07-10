"""
Unit tests for common enumerations.
"""

from src.common.enums import ConfigCategory, Environment


def test_config_category_values() -> None:
    """Verify configuration category values."""

    assert ConfigCategory.METRICS == "metrics"
    assert ConfigCategory.SERVICES == "services"
    assert ConfigCategory.SCENARIOS == "scenarios"
    assert ConfigCategory.SIMULATOR == "simulator"
    assert ConfigCategory.ENVIRONMENTS == "environments"


def test_environment_values() -> None:
    """Verify environment values."""

    assert Environment.DEVELOPMENT == "development"
    assert Environment.STAGING == "staging"
    assert Environment.PRODUCTION == "production"