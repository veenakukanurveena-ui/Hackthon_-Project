import re
from datetime import datetime

ALLOWED_FIELDS = {
    "timestamp",
    "host_id",
    "service",
    "severity",
    "event_type",
    "metric",
    "value",
    "unit",
    "anomaly_score"
}

ALLOWED_SEVERITIES = {"INFO", "WARNING", "ERROR", "CRITICAL"}

ALLOWED_UNITS = {
    "percent",
    "count",
    "milliseconds",
    "seconds",
    "bytes"
}

SAFE_NAME = re.compile(r"^[a-zA-Z0-9_.-]{1,64}$")


def contains_sensitive_data(value):
    text = str(value)

    patterns = [
        r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]"
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def validate_telemetry(data):

    if not isinstance(data, dict):
        return False, "Payload must be a JSON object", None

    # Reject additional or unapproved fields
    extra_fields = set(data.keys()) - ALLOWED_FIELDS

    if extra_fields:
        return False, "Unapproved fields detected", None

    # Check required fields
    missing_fields = ALLOWED_FIELDS - set(data.keys())

    if missing_fields:
        return False, "Required fields are missing", None

    # Check all text fields for sensitive information
    for field in ALLOWED_FIELDS:
        if isinstance(data[field], str) and contains_sensitive_data(data[field]):
            return False, "Sensitive information detected", None

    # Validate timestamp
    try:
        datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        )
    except (ValueError, AttributeError):
        return False, "Invalid timestamp", None

    # Validate names
    for field in ("host_id", "service", "event_type", "metric"):
        if not isinstance(data[field], str) or not SAFE_NAME.fullmatch(data[field]):
            return False, f"Invalid {field}", None

    # Validate severity
    if data["severity"] not in ALLOWED_SEVERITIES:
        return False, "Invalid severity", None

    # Validate unit
    if data["unit"] not in ALLOWED_UNITS:
        return False, "Invalid unit", None

    # Validate numeric values
    if isinstance(data["value"], bool) or not isinstance(data["value"], (int, float)):
        return False, "Metric value must be numeric", None

    if isinstance(data["anomaly_score"], bool) or not isinstance(data["anomaly_score"], (int, float)):
        return False, "Anomaly score must be numeric", None

    if not 0 <= data["anomaly_score"] <= 1:
        return False, "Anomaly score must be between 0 and 1", None

    if not 0 <= data["value"] <= 1_000_000_000:
        return False, "Metric value is outside allowed range", None

    # Return only explicitly approved fields
    safe_data = {field: data[field] for field in ALLOWED_FIELDS}

    return True, "Telemetry validated successfully", safe_data