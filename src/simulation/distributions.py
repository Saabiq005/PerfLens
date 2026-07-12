"""
Statistical distribution engine for the PerfLens simulator.

Purpose:
    Generate synthetic metric values using configurable
    statistical distributions.

Responsibilities:
    - Register supported distributions.
    - Generate values from registered distributions.
    - Provide deterministic random number generation.

This module does NOT:
    - Generate telemetry events.
    - Know about scenarios.
    - Know about services.
"""

from __future__ import annotations

import random
from collections.abc import Callable

from src.config.exceptions import ConfigurationValidationError


class DistributionEngine:
    """
    Registry-based statistical distribution engine.
    """

    _rng = random.Random()

    _registry: dict[
        str,
        Callable[[float, float], float],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
    ):
        """
        Decorator used to register a distribution function.
        """
        def decorator(
            function: Callable[[float, float], float],
        ) -> Callable[[float, float], float]:
            cls._registry[name.lower()] = function
            return function

        return decorator

    @classmethod
    def generate(
        cls,
        distribution: str,
        baseline: float,
        variance: float,
    ) -> float:
        """
        Generate a metric value.

        Raises
        ------
        ConfigurationValidationError
            If the distribution is unsupported.
        """
        generator = cls._registry.get(distribution.lower())

        if generator is None:
            supported = ", ".join(sorted(cls._registry))
            raise ConfigurationValidationError(
                message=(
                    f"Unsupported distribution '{distribution}'. "
                    f"Supported distributions: {supported}"
                ),
            )

        return generator(baseline, variance)

    @classmethod
    def supported_distributions(
        cls,
    ) -> tuple[str, ...]:
        """
        Return supported distributions.
        """
        return tuple(sorted(cls._registry))

    @classmethod
    def set_seed(
        cls,
        seed: int,
    ) -> None:
        """
        Seed the random number generator.
        """
        cls._rng.seed(seed)


# ============================================================================
# Registered Distribution Implementations
# ============================================================================

@DistributionEngine.register("normal")
def _normal(
    baseline: float,
    variance: float,
) -> float:
    """
    Generate a normally distributed value.

    Approximately 99.73% of generated values lie within
    baseline ± variance.
    """

    if variance == 0:
        return baseline

    sigma = variance / 3.0

    value = DistributionEngine._rng.gauss(
        baseline,
        sigma,
    )

    return max(
        0.0,
        value,
    )