def detect_anomaly(data):
    metric = data["metric"].lower()
    value = float(data["value"])
    score = float(data["anomaly_score"])
    severity = data["severity"].upper()

    risk_level = "LOW"
    reasons = []

    if metric == "cpu_usage":
        if value >= 90:
            risk_level = "CRITICAL"
            reasons.append("CPU usage exceeded 90%")
        elif value >= 80:
            risk_level = "HIGH"
            reasons.append("CPU usage is unusually high")

    elif metric == "memory_usage":
        if value >= 90:
            risk_level = "CRITICAL"
            reasons.append("Memory usage exceeded 90%")
        elif value >= 80:
            risk_level = "HIGH"
            reasons.append("Memory usage is unusually high")

    elif metric == "disk_usage":
        if value >= 95:
            risk_level = "CRITICAL"
            reasons.append("Disk usage exceeded 95%")
        elif value >= 85:
            risk_level = "HIGH"
            reasons.append("Disk usage is unusually high")

    if score >= 0.90:
        risk_level = "CRITICAL"
        reasons.append("High anomaly score detected")
    elif score >= 0.75 and risk_level == "LOW":
        risk_level = "HIGH"
        reasons.append("Unusual system behaviour detected")

    if severity == "CRITICAL":
        risk_level = "CRITICAL"
        reasons.append("Source event marked CRITICAL")
    elif severity == "ERROR" and risk_level == "LOW":
        risk_level = "MEDIUM"
        reasons.append("Source event marked ERROR")

    if not reasons:
        reasons.append("No configured anomaly threshold exceeded")

    return {
        "risk_level": risk_level,
        "is_anomaly": risk_level in ("HIGH", "CRITICAL"),
        "explanation": reasons
    }