# src/run_simulator.py
from pathlib import Path
from src.config.loader import ConfigurationLoader
from src.config.registry import ConfigurationRegistry
from src.mappers.runtime_registry import RuntimeRegistry
from src.simulation.event_factory import EventFactory
from src.simulation.simulator import Simulator
from src.telemetry.provider import TelemetryProvider
from src.telemetry.instrument_registry import InstrumentRegistry
from src.telemetry.metric_recorder import MetricRecorder
from src.telemetry.exporters.otlp import OTLPExporter
# 1. Boot up the configuration registry ecosystem
loader = ConfigurationLoader(Path("configs"))
config_registry = ConfigurationRegistry(loader)
config_registry.load()

# 2. Extract service configuration mappings into runtime domain models
runtime_registry = RuntimeRegistry.from_configuration(config_registry)
service = runtime_registry.service("inventory_service")

# 3. Setup OpenTelemetry instrumentation pipelines
telemetry_provider = TelemetryProvider(
    service_name=service.display_name,
    service_version=service.version
)
instrument_registry = InstrumentRegistry(meter=telemetry_provider.meter)
metric_recorder = MetricRecorder(registry=instrument_registry)

# 4. Inject the recorder into the EventFactory
factory = EventFactory(metric_recorder=metric_recorder)

# 5. Initialize the core telemetry simulator engine
simulator = Simulator(
    runtime_registry=runtime_registry,
    service_id="inventory_service",
    event_factory=factory
)

print("--- Triggering simulator.next_event() ---")

# 6. Execute the target snippet to tick the loop lifecycle forward
event = simulator.next_event()

print("\n--- Event Validated Successfully ---")
print(f"Generated Event ID: {event.event_id}")
print(f"Metrics Captured:   {event.metrics}")