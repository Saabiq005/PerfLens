"""
Scenario lifecycle engine for the PerfLens simulator.
"""

from __future__ import annotations

import random

from src.mappers.runtime_registry import RuntimeRegistry
from src.models.scenario import Scenario
from src.models.service import Service


class ScenarioEngine:
    """
    Maintains the current runtime scenario.
    """

    def __init__(
        self,
        service: Service,
        runtime_registry: RuntimeRegistry,
    ) -> None:

        self._service = service

        self._runtime_registry = runtime_registry

        self._rng = random.Random()

        self._current_scenario = runtime_registry.scenario(
            service.initial_scenario,
        )

        self._remaining_duration = (
            self._next_duration(
                self._current_scenario,
            )
        )

    # ===================================================================

    def current(
        self,
    ) -> Scenario:
        """
        Return the active scenario.
        """
        return self._current_scenario

    # ===================================================================

    def next(
        self,
    ) -> Scenario:
        """
        Advance the simulation by one tick and return the active scenario.
        """

        self._remaining_duration -= 1

        if self._remaining_duration <= 0:

            self._transition()

        return self._current_scenario

    # ===================================================================

    def _transition(
        self,
    ) -> None:

        transitions = self._current_scenario.transitions

        population = list(
            transitions.keys(),
        )

        weights = list(
            transitions.values(),
        )

        scenario_id = self._rng.choices(
            population,
            weights=weights,
            k=1,
        )[0]

        self._current_scenario = (
            self._runtime_registry.scenario(
                scenario_id,
            )
        )

        self._remaining_duration = (
            self._next_duration(
                self._current_scenario,
            )
        )

    # ===================================================================

    def _next_duration(
        self,
        scenario: Scenario,
    ) -> int:

        minimum, maximum = (
            scenario.duration_range
        )

        return self._rng.randint(
            minimum,
            maximum,
        )