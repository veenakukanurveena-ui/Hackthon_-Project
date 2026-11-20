import json
from datetime import datetime
import math


REQUIRED_FIELDS = {
    "operating_system",
    "cpu_usage_percent",
    "ram_usage_percent",
    "disk_usage_percent",
    "timestamp"
}


def validate_metrics(metrics):

    # Check that the input is a dictionary
    if not isinstance(metrics, dict):
        return False, "Data must be a JSON object."

    # Check that only approved fields exist
    if set(metrics.keys()) != REQUIRED_FIELDS:
        return False, "Missing or unexpected fields."

    # Check operating system
    if not isinstance(metrics["operating_system"], str):
        return False, "Invalid operating system."

    if not metrics["operating_system"]:
        return False, "Operating system cannot be empty."

    # Check CPU, RAM and disk values
    for field in [
        "cpu_usage_percent",
        "ram_usage_percent",
        "disk_usage_percent"
    ]:
        value = metrics[field]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False, f"{field} must be a number."

        if not math.isfinite(value) or not 0 <= value <= 100:
            return False, f"{field} must be between 0 and 100."

    # Check timestamp
    try:
        datetime.fromisoformat(metrics["timestamp"])
    except (ValueError, TypeError):
        return False, "Invalid timestamp."

    return True, "Metrics are valid."


if __name__ == "__main__":

    with open("approved_metrics.json", "r") as file:
        metrics = json.load(file)

    valid, message = validate_metrics(metrics)

    print(message)
    test_metrics = {
        "operating_system": "Windows",
        "cpu_usage_percent": 150,
        "ram_usage_percent": 65,
        "disk_usage_percent": 48,
        "timestamp": "2026-11-20T10:30:00"
    }

    valid, message = validate_metrics(test_metrics)

    print(message)
if __name__ == "__main__":

    # Test 1: Valid metrics
    valid_metrics = {
        "operating_system": "Windows",
        "cpu_usage_percent": 50,
        "ram_usage_percent": 65,
        "disk_usage_percent": 48,
        "timestamp": "2026-11-20T10:30:00"
    }

    # Test 2: Invalid metrics
    invalid_metrics = valid_metrics.copy()
    invalid_metrics["cpu_usage_percent"] = 150

    # Run valid test
    result1, message1 = validate_metrics(valid_metrics)

    print("VALID DATA TEST:")
    print(message1)

    # Run invalid test
    result2, message2 = validate_metrics(invalid_metrics)

    print("\nINVALID DATA TEST:")
    print(message2)