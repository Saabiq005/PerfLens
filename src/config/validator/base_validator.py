"""
Base validation framework for the PerfLens configuration system.

Purpose:
    Defines the abstract base class for all configuration validators
    and provides reusable validation helper methods.

Responsibilities:
    - Define the validator interface.
    - Provide generic validation helpers.
    - Raise consistent validation exceptions.

This module does NOT:
    - Contain business validation logic.
    - Understand configuration types.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from __future__ import annotations

from abc import ABC, abstractmethod
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
    def validate(self, data: dict[str, Any]) -> None:
        """
        Validate configuration data.

        Args:
            data:
                Configuration dictionary.

        Raises:
            ConfigurationValidationError:
                If validation fails.
        """
        raise NotImplementedError

    def _require_field(
        self,
        data: dict[str, Any],
        field: str,
    ) -> Any:
        """
        Require a field to exist.

        Args:
            data:
                Configuration dictionary.

            field:
                Required field name.

        Returns:
            Field value.

        Raises:
            ConfigurationValidationError:
                If the field is missing.
        """
        if field not in data:
            self._raise_validation_error(
                f"Missing required field '{field}'."
            )

        return data[field]

    def _require_fields(
        self,
        data: dict[str, Any],
        fields: list[str],
    ) -> None:
        """
        Require multiple fields.
        """
        for field in fields:
            self._require_field(data, field)

    def _require_type(
        self,
        value: Any,
        expected_type: type,
        field_name: str,
    ) -> None:
        """
        Validate the type of a value.
        """
        if not isinstance(value, expected_type):
            self._raise_validation_error(
                f"Field '{field_name}' must be "
                f"of type '{expected_type.__name__}'."
            )

    def _require_non_empty(
        self,
        value: Any,
        field_name: str,
    ) -> None:
        """
        Require a value to be non-empty.
        """
        if value in (None, "", [], {}, ()):
            self._raise_validation_error(
                f"Field '{field_name}' cannot be empty."
            )

    def _raise_validation_error(
        self,
        message: str,
    ) -> None:
        """
        Raise a standardized validation exception.
        """
        raise ConfigurationValidationError(message)