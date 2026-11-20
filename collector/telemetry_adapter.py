def convert_to_telemetry(metrics):
    events = []

    metric_fields = [
        ("cpu_usage_percent", "cpu_usage", "percent"),
        ("ram_usage_percent", "ram_usage", "percent"),
        ("disk_usage_percent", "disk_usage", "percent"),
    ]

    for field, metric_name, unit in metric_fields:
        events.append({
            "timestamp": metrics["timestamp"],
            "host_id": "local-device",
            "service": "system-monitor",
            "severity": "INFO",
            "event_type": "system_metric",
            "metric": metric_name,
            "value": metrics[field],
            "unit": unit,
            "anomaly_score": 0.0
        })

    return events