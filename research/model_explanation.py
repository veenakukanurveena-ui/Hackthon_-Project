class ModelExplainer:

    def explain(self, telemetry, prediction):

        feature_scores = {
            "cpu_usage": telemetry.get("cpu_usage", 0),
            "memory_usage": telemetry.get("memory_usage", 0),
            "disk_usage": telemetry.get("disk_usage", 0),
            "latency_ms": telemetry.get("latency_ms", 0),
            "packet_loss_pct": telemetry.get("packet_loss_pct", 0),
            "failed_login_count": telemetry.get("failed_login_count", 0)
        }

        thresholds = {
            "cpu_usage": 90,
            "memory_usage": 90,
            "disk_usage": 90,
            "latency_ms": 150,
            "packet_loss_pct": 5,
            "failed_login_count": 10
        }

        reasons = []

        for feature, value in feature_scores.items():

            if value >= thresholds[feature]:
                reasons.append({
                    "metric": feature,
                    "observed_value": value,
                    "configured_threshold": thresholds[feature],
                    "reason": f"{feature} exceeded its configured threshold."
                })

        if prediction == "Anomaly" and not reasons:
            summary = (
                "The AI model detected an unusual pattern, "
                "but no individual threshold was exceeded."
            )

        elif reasons:
            summary = "One or more telemetry metrics exceeded configured thresholds."

        else:
            summary = "No configured threshold violations were identified."

        return {
            "prediction": prediction,
            "explanation": summary,
            "contributing_metrics": reasons,
            "explanation_type": "Threshold-based feature explanation",
            "warning": (
                "These metrics are supporting evidence, "
                "not proof of causation."
            )
        }


if __name__ == "__main__":

    sample = {
        "cpu_usage": 98,
        "memory_usage": 95,
        "disk_usage": 60,
        "latency_ms": 200,
        "packet_loss_pct": 0,
        "failed_login_count": 2
    }

    explainer = ModelExplainer()

    result = explainer.explain(sample, "Anomaly")

    print("\nAI Model Explanation:")

    for key, value in result.items():
        print(f"{key}: {value}")