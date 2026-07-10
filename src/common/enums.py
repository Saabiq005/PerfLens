"""
Enumerations used throughout the PerfLens project.

Purpose:
    Provides strongly typed constants shared across the application.

Responsibilities:
    - Define project-wide enumerations.
    - Eliminate magic strings.
    - Improve readability and type safety.

This module does NOT:
    - Contain business logic.
    - Read configuration files.
    - Perform validation.
"""

# ============================================================================
# Standard Library Imports
# ============================================================================

from enum import StrEnum


# ============================================================================
# Configuration Enums
# ============================================================================

class ConfigCategory(StrEnum):
    """
    Supported configuration categories.

    These values correspond to the directory names
    inside the project's `configs/` folder.
    """

    METRICS = "metrics"
    SERVICES = "services"
    SCENARIOS = "scenarios"
    SIMULATOR = "simulator"
    ENVIRONMENTS = "environments"


class Environment(StrEnum):
    """
    Supported deployment environments.
    """

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"