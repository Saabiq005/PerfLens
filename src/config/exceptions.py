"""
Custom exception hierarchy for the PerfLens project.

Purpose:
    Defines the exception hierarchy used throughout the PerfLens
    application.

Responsibilities:
    - Provide a common root exception.
    - Standardize error reporting.
    - Support structured diagnostic information.
    - Enable subsystem-specific exception hierarchies.

This module does NOT:
    - Read configuration files.
    - Validate configuration.
    - Perform logging.
    - Handle error recovery.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from typing import Any


# ============================================================================
# Classes
# ============================================================================

class PerfLensError(Exception):
    """
    Base exception for all PerfLens-specific errors.

    Every custom exception in the PerfLens project should inherit from
    this class.

    Attributes:
        message:
            Human-readable description of the error.

        details:
            Optional structured diagnostic information.
    """

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize a PerfLensError.

        Args:
            message:
                Human-readable error description.

            details:
                Optional dictionary containing additional debugging
                information.
        """
        super().__init__(message)

        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """
        Return the exception message.

        Returns:
            Human-readable error message.
        """
        return self.message


class ConfigurationError(PerfLensError):
    """
    Base exception for all configuration-related errors.

    Extends PerfLensError by including configuration-specific context.

    Attributes:
        config_type:
            Type of configuration involved
            (metric, scenario, service, simulator, environment).

        config_name:
            Identifier or name of the configuration object.
    """

    def __init__(
        self,
        message: str,
        config_type: str | None = None,
        config_name: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize a ConfigurationError.

        Args:
            message:
                Human-readable error description.

            config_type:
                Configuration category.

            config_name:
                Configuration identifier.

            details:
                Optional structured diagnostic information.
        """
        super().__init__(
            message=message,
            details=details,
        )

        self.config_type = config_type
        self.config_name = config_name

    def __str__(self) -> str:
        """
        Return a formatted configuration error.

        Returns:
            Human-readable configuration error including
            configuration context when available.
        """
        context = []

        if self.config_type:
            context.append(f"type='{self.config_type}'")

        if self.config_name:
            context.append(f"name='{self.config_name}'")

        if context:
            return f"{self.message} ({', '.join(context)})"

        return self.message


class ConfigurationNotFoundError(ConfigurationError):
    """
    Raised when a required configuration file or directory
    cannot be found.
    """

    pass


class ConfigurationValidationError(ConfigurationError):
    """
    Raised when configuration data fails validation.
    """

    pass


class DuplicateConfigurationError(ConfigurationError):
    """
    Raised when duplicate configuration identifiers
    are detected.
    """

    pass


class UnsupportedConfigurationError(ConfigurationError):
    """
    Raised when an unsupported configuration value
    is encountered.
    """

    pass