class RecommendationEngine:

    def generate(self, telemetry):

        recommendations = []

        def add_recommendation(
            category, issue, priority, action, reason
        ):
            recommendations.append({
                "category": category,
                "issue": issue,
                "priority": priority,
                "recommended_action": action,
                "reason": reason,
                "requires_human_approval": True
            })

        cpu = telemetry.get("cpu_usage", 0)
        memory = telemetry.get("memory_usage", 0)
        disk = telemetry.get("disk_usage", 0)
        latency = telemetry.get("latency_ms", 0)
        packet_loss = telemetry.get("packet_loss_pct", 0)
        failed_logins = telemetry.get("failed_login_count", 0)

        if cpu >= 90:
            add_recommendation(
                "Infrastructure",
                "High CPU utilization",
                "Critical",
                "Investigate CPU-intensive processes.",
                f"CPU usage reached {cpu}%."
            )

        elif cpu >= 75:
            add_recommendation(
                "Infrastructure",
                "Elevated CPU utilization",
                "Medium",
                "Monitor CPU trends and review running processes.",
                f"CPU usage reached {cpu}%."
            )

        if memory >= 90:
            add_recommendation(
                "Infrastructure",
                "High memory utilization",
                "Critical",
                "Investigate memory-intensive applications.",
                f"Memory usage reached {memory}%."
            )

        if disk >= 90:
            add_recommendation(
                "Storage",
                "High disk utilization",
                "High",
                "Review storage consumption and plan capacity expansion.",
                f"Disk usage reached {disk}%."
            )

        if latency >= 150:
            add_recommendation(
                "Network",
                "High network latency",
                "High",
                "Investigate network congestion and connectivity.",
                f"Latency reached {latency} ms."
            )

        if packet_loss >= 5:
            add_recommendation(
                "Network",
                "Packet loss detected",
                "High",
                "Inspect network links and packet transmission errors.",
                f"Packet loss reached {packet_loss}%."
            )

        if failed_logins >= 10:
            add_recommendation(
                "Security",
                "Repeated failed login attempts",
                "Critical",
                "Review authentication logs and investigate suspicious activity.",
                f"{failed_logins} failed logins were recorded."
            )

        if not recommendations:
            recommendations.append({
                "category": "Monitoring",
                "issue": "No major threshold violations",
                "priority": "Low",
                "recommended_action": "Continue monitoring telemetry.",
                "reason": "No configured thresholds were exceeded.",
                "requires_human_approval": False
            })

        return recommendations


if __name__ == "__main__":

    sample_telemetry = {
        "cpu_usage": 98,
        "memory_usage": 95,
        "disk_usage": 92,
        "latency_ms": 200,
        "packet_loss_pct": 10,
        "failed_login_count": 15
    }

    engine = RecommendationEngine()

    results = engine.generate(sample_telemetry)

    print("\nAI Recommendations:")

    for item in results:
        print(item)
    