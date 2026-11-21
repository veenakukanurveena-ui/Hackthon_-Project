import json
import time

from system_metrics import collect_system_metrics
from privacy_filter import redact_sensitive_data
from data_validator import validate_metrics
from anomaly_detector import detect_anomalies


def run_collector():
    print("\nCollecting system metrics...")

    # Step 1: Collect system metrics
    metrics = collect_system_metrics()

    # Step 2: Select only approved information
    approved_metrics = {
        "operating_system": metrics["operating_system"],
        "cpu_usage_percent": metrics["cpu_usage_percent"],
        "ram_usage_percent": metrics["ram_usage_percent"],
        "disk_usage_percent": metrics["disk_usage_percent"],
        "timestamp": metrics["timestamp"]
    }

    # Step 3: Validate the collected data
    valid, message = validate_metrics(approved_metrics)

    if not valid:
        print("Validation failed:", message)
        return

    print("Validation successful!")

    # Step 4: Detect unusual system usage
    alerts = detect_anomalies(approved_metrics)

    print("\nANOMALY DETECTION RESULTS:")

    for alert in alerts:
        print(alert)

    # Step 5: Convert approved metrics into JSON
    json_data = json.dumps(approved_metrics, indent=4)

    # Step 6: Apply privacy filtering
    safe_data = redact_sensitive_data(json_data)

    # Step 7: Save approved data locally
    with open("approved_metrics.json", "w") as file:
        file.write(safe_data)

    print("\nMetrics saved successfully!")
    print("\nAPPROVED METRICS:")
    print(safe_data)


def start_monitoring():
    print("================================")
    print("     LOCAL COLLECTOR STARTED")
    print("================================")
    print("Monitoring interval: 10 seconds")
    print("Press CTRL+C to stop monitoring.")

    try:
        while True:
            run_collector()
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nLocal Collector stopped.")


if __name__ == "__main__":
    start_monitoring()
    