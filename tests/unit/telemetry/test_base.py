"""
Unit tests for BaseExporter.
"""

from __future__ import annotations

import pytest

from src.telemetry.exporters.base import BaseExporter


def test_base_exporter_cannot_be_instantiated() -> None:
    """
    Verify BaseExporter is abstract.
    """

    with pytest.raises(TypeError):
        BaseExporter()