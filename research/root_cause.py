class RootCauseAnalyzer:

    def analyze(self, telemetry):

        possible_causes = []
        supporting_evidence = []
        investigations = []
        confidence_scores = []

        checks = [
            (
                "High CPU utilization",
                "cpu_usage",
                90,
                "CPU utilization is critically elevated.",
                "Inspect running processes and application workload."
            ),
            (
                "High memory utilization",
                "memory_usage",
                90,
                "Memory utilization is critically elevated.",
                "Inspect memory-consuming processes and memory leaks."
            ),
            (
                "High disk utilization",
                "disk_usage",
                90,
                "Disk utilization is critically elevated.",
                "Inspect disk capacity and storage consumption."
            ),
            (
                "High network latency",
                "latency_ms",
                150,
                "Network latency is above the expected threshold.",
                "Inspect network routes, bandwidth and server response time."
            ),
            (
                "High packet loss",
                "packet_loss_pct",
                5,
                "Packet loss indicates possible network instability.",
                "Inspect network interfaces and packet transmission errors."
            ),
            (
                "Repeated failed login attempts",
                "failed_login_count",
                10,
                "Multiple failed login attempts were detected.",
                "Review authentication logs and investigate suspicious activity."
            )
        ]

        for name, metric, threshold, evidence, investigation in checks:

            value = telemetry.get(metric, 0)

            if value is None:
                continue

            try:
                value = float(value)
            except (ValueError, TypeError):
                continue

            if value >= threshold:

                possible_causes.append(name)

                supporting_evidence.append({
                    "metric": metric,
                    "observed_value": value,
                    "threshold": threshold,
                    "evidence": evidence
                })

                investigations.append(investigation)

                score = min(
                    95,
                    60 + ((value - threshold) / threshold) * 20
                )

                confidence_scores.append(score)

        confidence = (
            round(sum(confidence_scores) / len(confidence_scores), 2)
            if confidence_scores else 0
        )

        return {
            "type": "Rule-based assistance",
            "analysis_type": "Rule-based root cause assistance",
            "possible_contributing_factors": possible_causes,
            "possible_causes": possible_causes,
            "supporting_evidence": supporting_evidence,
            "recommended_investigations": investigations,
            "confidence_score": confidence,
            "confidence_note": (
                "Heuristic indicator score, not a statistically "
                "calibrated probability."
            ),
            "warning": (
                "These are possible contributing factors. "
                "They do not establish confirmed root causes."
            )
        }


if __name__ == "__main__":

    sample_telemetry = {
        "cpu_usage": 96,
        "memory_usage": 93,
        "disk_usage": 60,
        "latency_ms": 180,
        "packet_loss_pct": 8,
        "failed_login_count": 12
    }

    analyzer = RootCauseAnalyzer()
    print(analyzer.analyze(sample_telemetry))