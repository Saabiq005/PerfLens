"""
Unit tests for the PerfLens configuration exception hierarchy.

Purpose:
    Verify the behavior and inheritance of all custom exceptions
    defined in the configuration framework.

Responsibilities:
    - Validate inheritance relationships.
    - Verify exception attributes.
    - Verify string representations.
    - Verify polymorphic exception handling.

This module does NOT:
    - Test configuration loading.
    - Test configuration validation.
    - Test file system interactions.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

# None

# ============================================================================
# Third-Party Imports
# ============================================================================

import pytest

# ============================================================================
# Local Imports
# ============================================================================

from src.config.exceptions import (
    ConfigurationError,
    ConfigurationNotFoundError,
    ConfigurationValidationError,
    DuplicateConfigurationError,
    PerfLensError,
    UnsupportedConfigurationError,
)

# ============================================================================
# PerfLensError Tests
# ============================================================================


def test_perf_lens_error_stores_message() -> None:
    """Verify that the exception stores the provided message."""

    error = PerfLensError("Something went wrong.")

    assert error.message == "Something went wrong."


def test_perf_lens_error_stores_details() -> None:
    """Verify that diagnostic details are stored."""

    details = {"field": "latency"}

    error = PerfLensError(
        message="Validation failed.",
        details=details,
    )

    assert error.details == details


def test_perf_lens_error_string_representation() -> None:
    """Verify the string representation of the exception."""

    error = PerfLensError("Test message.")

    assert str(error) == "Test message."


# ============================================================================
# ConfigurationError Tests
# ============================================================================


def test_configuration_error_stores_context() -> None:
    """Verify configuration context is preserved."""

    error = ConfigurationError(
        message="Configuration error.",
        config_type="scenario",
        config_name="healthy",
    )

    assert error.config_type == "scenario"
    assert error.config_name == "healthy"


def test_configuration_error_string_representation() -> None:
    """Verify formatted configuration error output."""

    error = ConfigurationError(
        message="Invalid configuration.",
        config_type="metric",
        config_name="latency",
    )

    expected = (
        "Invalid configuration. "
        "(type='metric', name='latency')"
    )

    assert str(error) == expected


def test_configuration_error_without_context() -> None:
    """Verify string output without configuration context."""

    error = ConfigurationError(
        message="Generic configuration error."
    )

    assert str(error) == "Generic configuration error."


# ============================================================================
# Inheritance Tests
# ============================================================================


@pytest.mark.parametrize(
    "exception_class",
    [
        ConfigurationNotFoundError,
        ConfigurationValidationError,
        DuplicateConfigurationError,
        UnsupportedConfigurationError,
    ],
)
def test_specialized_exceptions_inherit_configuration_error(
    exception_class,
) -> None:
    """Verify all specialized exceptions inherit ConfigurationError."""

    assert issubclass(exception_class, ConfigurationError)


@pytest.mark.parametrize(
    "exception_class",
    [
        ConfigurationNotFoundError,
        ConfigurationValidationError,
        DuplicateConfigurationError,
        UnsupportedConfigurationError,
    ],
)
def test_specialized_exceptions_inherit_perf_lens_error(
    exception_class,
) -> None:
    """Verify all specialized exceptions inherit PerfLensError."""

    assert issubclass(exception_class, PerfLensError)


# ============================================================================
# Polymorphism Tests
# ============================================================================


def test_configuration_error_polymorphism() -> None:
    """
    Verify specialized exceptions can be caught as ConfigurationError.
    """

    with pytest.raises(ConfigurationError):

        raise ConfigurationValidationError(
            message="Missing required field."
        )


def test_perf_lens_error_polymorphism() -> None:
    """
    Verify configuration exceptions can be caught as PerfLensError.
    """

    with pytest.raises(PerfLensError):

        raise ConfigurationValidationError(
            message="Missing required field."
        )


# ============================================================================
# Attribute Tests
# ============================================================================


def test_specialized_exception_inherits_attributes() -> None:
    """Verify inherited attributes are available."""

    error = ConfigurationValidationError(
        message="Invalid metric.",
        config_type="metric",
        config_name="latency",
        details={"field": "unit"},
    )

    assert error.message == "Invalid metric."
    assert error.config_type == "metric"
    assert error.config_name == "latency"
    assert error.details == {"field": "unit"}