def detect_anomalies(metrics):

    alerts = []

    # Check CPU usage
    if metrics["cpu_usage_percent"] >= 90:
        alerts.append("WARNING: High CPU usage!")

    # Check RAM usage
    if metrics["ram_usage_percent"] >= 90:
        alerts.append("WARNING: High RAM usage!")

    # Check Disk usage
    if metrics["disk_usage_percent"] >= 90:
        alerts.append("WARNING: High Disk usage!")

    if not alerts:
        alerts.append("System status: NORMAL")

    return alerts


if __name__ == "__main__":

    # Sample system metrics
    test_metrics = {
        "cpu_usage_percent": 45,
        "ram_usage_percent": 96,
        "disk_usage_percent": 95
    }

    results = detect_anomalies(test_metrics)

    print("ANOMALY DETECTION RESULTS")

    for alert in results:
        print(alert)