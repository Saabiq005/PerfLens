# src/run_phase10.py
import time
import gc
import tracemalloc
import warnings
from pathlib import Path
from src.app.application import Application

def run_long_validation():
    # 1. Enable standard library tracing hooks to catch allocations and warnings
    tracemalloc.start()
    warnings.simplefilter("always", ResourceWarning)
    
    # Initialize your primary application entry point context
    app = Application(
        configuration_directory=Path("configs")
    )
    
    app.initialize()
    
    # 2. Configure time bounds (10 minutes = 600 seconds)
    duration_seconds = 600
    start_time = time.time()
    end_time = start_time + duration_seconds
    
    print(f"🚀 Phase 10: Long Running Validation Started at {time.ctime(start_time)}")
    print(f"⌛ Engine will execute continuously for 10 minutes (until {time.ctime(end_time)})...")
    
    event_count = 0
    snapshot_interval = 60  # Print an intermediate health check snapshot every 60 seconds
    next_snapshot = start_time + snapshot_interval
    
    # Take an initial memory snapshot baseline
    gc.collect()
    initial_mem, _ = tracemalloc.get_traced_memory()
    
    try:
        # Instead of an infinite block loop, bound the run to the target duration window
        while time.time() < end_time:
            # Generate a discrete synthetic event tick context
            # This triggers ScenarioEngine advances, EventFactory builds, and MetricRecorder updates
            event = app._simulator.next_event()
            event_count += 1
            
            # Briefly throttle to prevent extreme CPU exhaustion during local simulation test runs
            time.sleep(0.05)
            
            # Print intermediate health checks
            current_time = time.time()
            if current_time >= next_snapshot:
                gc.collect()
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                elapsed = int(current_time - start_time)
                print(
                    f"⏱️ [{elapsed}s elapsed] Events generated: {event_count} | "
                    f"Current Memory: {current_mem / 1024 / 1024:.2f} MB | "
                    f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB"
                )
                next_snapshot += snapshot_interval

    except Exception as e:
        print(f"\n❌ CRITICAL: Validation Interrupted by an Exception: {e}")
        raise e
    finally:
        # 3. Finalization Analysis Report
        actual_end = time.time()
        gc.collect()
        final_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print("\n========================================================")
        print("📊 PHASE 10 SUMMARY REPORT")
        print("========================================================")
        print(f"🟢 Total Runtime: {int(actual_end - start_time)} seconds")
        print(f"📦 Total Events Processed: {event_count}")
        print(f"📈 Peak Memory Consumption: {peak_mem / 1024 / 1024:.2f} MB")
        print(f"📉 Final Memory Growth: {(final_mem - initial_mem) / 1024:.2f} KB")
        print("========================================================")

if __name__ == "__main__":
    run_long_validation()