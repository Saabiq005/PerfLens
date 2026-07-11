"""
Base validation framework for the PerfLens configuration system.

Purpose:
    Defines the abstract base class for all configuration validators
    and provides reusable validation helper methods.

Responsibilities:
    - Define the validator interface.
    - Provide reusable validation helpers.
    - Raise consistent validation exceptions.

This module does NOT:
    - Understand business rules.
    - Load configuration files.
    - Modify configuration.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================

from src.config.exceptions import ConfigurationValidationError


# ============================================================================
# Classes
# ============================================================================


class BaseValidator(ABC):
    """
    Abstract base class for all configuration validators.
    """

    @abstractmethod
    def validate(
        self,
        configuration: Mapping[str, Any],
    ) -> None:
        """
        Validate a configuration.

        Args:
            configuration:
                Configuration to validate.

        Raises:
            ConfigurationValidationError:
                If validation fails.
        """
        raise NotImplementedError

    # =======================================================================
    # Required Field Validation
    # =======================================================================

    def _require_field(
        self,
        configuration: Mapping[str, Any],
        field: str,
    ) -> Any:
        """
        Ensure a required field exists.

        Args:
            configuration:
                Configuration mapping.

            field:
                Required field.

        Returns:
            Value associated with the field.

        Raises:
            ConfigurationValidationError:
                If the field is missing.
        """
        if field not in configuration:
            self._raise_validation_error(
                f"Missing required field '{field}'."
            )

        return configuration[field]

    def _require_fields(
        self,
        configuration: Mapping[str, Any],
        fields: list[str],
    ) -> None:
        """
        Ensure multiple required fields exist.
        """
        for field in fields:
            self._require_field(
                configuration,
                field,
            )

    # =======================================================================
    # Type Validation
    # =======================================================================

    def _require_type(
        self,
        value: Any,
        expected_type: type,
        field_name: str,
    ) -> None:
        """
        Ensure a value has the expected type.
        """
        if not isinstance(value, expected_type):
            self._raise_validation_error(
                f"Field '{field_name}' must be of type "
                f"'{expected_type.__name__}'."
            )

    # =======================================================================
    # Value Validation
    # =======================================================================

    def _require_non_empty(
        self,
        value: Any,
        field_name: str,
    ) -> None:
        """
        Ensure a value is not empty.
        """
        if value is None:
            self._raise_validation_error(
                f"Field '{field_name}' cannot be None."
            )

        if isinstance(value, str) and not value.strip():
            self._raise_validation_error(
                f"Field '{field_name}' cannot be empty."
            )

        if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
            self._raise_validation_error(
                f"Field '{field_name}' cannot be empty."
            )

    def _require_positive_number(
        self,
        value: int | float,
        field_name: str,
    ) -> None:
        """
        Ensure a numeric value is positive.
        """
        if value < 0:
            self._raise_validation_error(
                f"Field '{field_name}' must be greater than or equal to zero."
            )

    def _require_allowed_value(
        self,
        value: Any,
        allowed_values: list[Any],
        field_name: str,
    ) -> None:
        """
        Ensure a value belongs to an allowed set.
        """
        if value not in allowed_values:
            self._raise_validation_error(
                f"Field '{field_name}' contains an unsupported value "
                f"'{value}'."
            )

    def _require_unique(
        self,
        value: Any,
        seen_values: set[Any],
        field_name: str,
    ) -> None:
        """
        Ensure a value is unique.
        """
        if value in seen_values:
            self._raise_validation_error(
                f"Duplicate value '{value}' found for '{field_name}'."
            )

        seen_values.add(value)

    # =======================================================================
    # Exception Helper
    # =======================================================================

    def _raise_validation_error(
        self,
        message: str,
    ) -> None:
        """
        Raise a standardized validation exception.
        """
        raise ConfigurationValidationError(message)