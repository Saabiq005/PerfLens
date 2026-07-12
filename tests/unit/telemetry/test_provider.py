from src.telemetry.provider import TelemetryProvider


def test_provider_creates_meter():

    provider = TelemetryProvider()

    assert provider.meter is not None