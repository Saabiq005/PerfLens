"""
Configuration loading framework for the PerfLens project.

Purpose:
    Provides functionality for locating and loading configuration
    files from the project's configuration directory.

Responsibilities:
    - Maintain the root configuration directory.
    - Serve as the entry point for configuration loading.

This module does NOT:
    - Validate configuration.
    - Cache configuration.
    - Create domain objects.
    - Perform application-specific processing.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from pathlib import Path

from typing import Any

import yaml
from yaml import YAMLError

# ============================================================================
# Local Imports
# ============================================================================

from src.common.enums import ConfigCategory

from src.config.exceptions import (
    ConfigurationNotFoundError,
    ConfigurationValidationError,
    UnsupportedConfigurationError,
)  


# ============================================================================
# Classes
# ============================================================================


class ConfigurationLoader:
    """
    Generic configuration loader for the PerfLens framework.

    This class is responsible for locating and loading configuration
    files. It intentionally has no knowledge of metrics, scenarios,
    services, environments, or other business concepts.

    Attributes:
        configuration_root:
            Absolute path to the project's configuration directory.
    """

    def __init__(self, configuration_root: Path) -> None:
        """
        Initialize the configuration loader.

        Args:
            configuration_root:
                Path to the project's configuration directory.

        Raises:
            ConfigurationNotFoundError:
                If the configuration directory does not exist or is not
                a directory.
        """
        if not configuration_root.exists():
            raise ConfigurationNotFoundError(
                message="Configuration root directory does not exist.",
                config_type="directory",
                config_name=str(configuration_root),
            )

        if not configuration_root.is_dir():
            raise ConfigurationNotFoundError(
                message="Configuration root is not a directory.",
                config_type="directory",
                config_name=str(configuration_root),
            )

        self._configuration_root = configuration_root.resolve()

    @property
    def configuration_root(self) -> Path:
        """
        Return the resolved configuration root directory.

        Returns:
            Absolute path to the configuration directory.
        """
        return self._configuration_root
    
    def resolve_path(
        self,
        category: ConfigCategory,
        filename: str,
    ) -> Path:
        """
        Resolve the absolute path to a configuration file.

        Args:
            category:
                Configuration category containing the file.

            filename:
                Name of the configuration file.

        Returns:
            Absolute path to the requested configuration file.

        Raises:
            ConfigurationNotFoundError:
                If the configuration category directory or the
                requested file does not exist.

            UnsupportedConfigurationError:
                If the filename does not have a supported YAML
                extension.
        """
        if not filename.endswith((".yaml", ".yml")):
            raise UnsupportedConfigurationError(
                message="Unsupported configuration file extension.",
                config_type=category.value,
                config_name=filename,
            )

        category_path = self.configuration_root / category.value

        if not category_path.exists():
            raise ConfigurationNotFoundError(
                message="Configuration category directory does not exist.",
                config_type="directory",
                config_name=str(category_path),
            )

        file_path = category_path / filename

        if not file_path.exists():
            raise ConfigurationNotFoundError(
                message="Configuration file does not exist.",
                config_type=category.value,
                config_name=filename,
            )

        return file_path.resolve()
    
    def exists(
        self,
        category: ConfigCategory,
        filename: str,
    ) -> bool:
        """
        Determine whether a configuration file exists.

        Args:
            category:
                Configuration category containing the file.

            filename:
                Configuration filename.

        Returns:
            True if the configuration file exists;
            otherwise False.
        """
        try:
            self.resolve_path(category, filename)
            return True

        except (
            ConfigurationNotFoundError,
            UnsupportedConfigurationError,
        ):
            return False
    
    def list_files(
        self,
        category: ConfigCategory,
    ) -> list[Path]:
        """
        List all supported configuration files within a category.

        Args:
            category:
                Configuration category to search.

        Returns:
            A sorted list of absolute paths to YAML configuration files.

        Raises:
            ConfigurationNotFoundError:
                If the configuration category directory does not exist.
        """
        category_path = self.configuration_root / category.value

        if not category_path.exists():
            raise ConfigurationNotFoundError(
                message="Configuration category directory does not exist.",
                config_type="directory",
                config_name=str(category_path),
            )

        files = [
            file.resolve()
            for file in category_path.iterdir()
            if file.is_file()
            and file.suffix.lower() in (".yaml", ".yml")
        ]

        return sorted(files)

    def load_file(
        self,
        category: ConfigCategory,
        filename: str,
    ) -> dict[str, Any]:
        """
        Load and deserialize a YAML configuration file.

        Args:
            category:
                Configuration category containing the file.

            filename:
                Name of the configuration file.

        Returns:
            Parsed YAML configuration as a dictionary.

        Raises:
            ConfigurationNotFoundError:
                If the configuration file does not exist.

            UnsupportedConfigurationError:
                If the file extension is not supported.

            ConfigurationValidationError:
                If the YAML file cannot be parsed.
        """
        file_path = self.resolve_path(category, filename)

        try:
            with file_path.open(
                mode="r",
                encoding="utf-8",
            ) as yaml_file:

                data = yaml.safe_load(yaml_file)

        except YAMLError as exc:
            raise ConfigurationValidationError(
                message="Failed to parse YAML configuration.",
                config_type=category.value,
                config_name=filename,
                details={"error": str(exc)},
            ) from exc

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise ConfigurationValidationError(
                message="Configuration root must be a YAML mapping.",
                config_type=category.value,
                config_name=filename,
            )

        return data    