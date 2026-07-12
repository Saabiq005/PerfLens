"""
OpenTelemetry instrument registry.

Purpose:
    Create and cache OpenTelemetry metric instruments.

Responsibilities:
    - Create instruments.
    - Cache instruments.
    - Return instruments.

This module does NOT:
    - Record metric values.
    - Configure MeterProvider.
    - Know about the simulator.
"""

from __future__ import annotations

from opentelemetry.metrics import Counter
from opentelemetry.metrics import Histogram
from opentelemetry.metrics import Meter

from src.models.metric import Metric


class InstrumentRegistry:
    """
    Registry of OpenTelemetry metric instruments.
    """

    _INSTRUMENT_MAPPING = {
        "latency": "histogram",
        "trace_duration": "histogram",
        "throughput": "counter",
        "error_rate": "gauge",
    }

    def __init__(
        self,
        meter: Meter,
    ) -> None:

        self._meter = meter

        self._instruments: dict[str, object] = {}

    # ===============================================================

    def instrument(
        self,
        metric: Metric,
    ) -> object:

        instrument = self._instruments.get(
            metric.metric_id,
        )

        if instrument is not None:
            return instrument

        instrument = self._create_instrument(
            metric,
        )

        self._instruments[
            metric.metric_id
        ] = instrument

        return instrument

    # ===============================================================

    def _create_instrument(
        self,
        metric: Metric,
    ) -> object:

        instrument_type = self._INSTRUMENT_MAPPING[
            metric.metric_id
        ]

        if instrument_type == "histogram":

            return self._meter.create_histogram(
                name=metric.metric_id,
                unit="ms",
                description=metric.metric_id,
            )

        if instrument_type == "counter":

            return self._meter.create_counter(
                name=metric.metric_id,
                unit="requests",
                description=metric.metric_id,
            )

        if instrument_type == "gauge":

            # Placeholder for MetricRecorder.
            # OpenTelemetry Python gauges are callback-based.
            return self._meter.create_up_down_counter(
                name=metric.metric_id,
                unit="percent",
                description=metric.metric_id,
            )

        raise RuntimeError(
            f"Unsupported instrument type: {instrument_type}"
        )