from research.model_explanation import ModelExplainer


def test_explains_anomaly_prediction():
    explainer = ModelExplainer()

    telemetry = {
        "cpu_usage": 96,
        "memory_usage": 92,
        "disk_usage": 50,
        "latency_ms": 180,
        "packet_loss_pct": 6,
        "failed_login_count": 12
    }

    result = explainer.explain(telemetry, "Anomaly")

    assert result["prediction"] == "Anomaly"
    assert len(result["contributing_metrics"]) > 0
    assert "explanation" in result


def test_explanation_contains_warning():
    explainer = ModelExplainer()

    telemetry = {
        "cpu_usage": 40,
        "memory_usage": 50,
        "disk_usage": 30,
        "latency_ms": 40,
        "packet_loss_pct": 0,
        "failed_login_count": 0
    }

    result = explainer.explain(telemetry, "Normal")

    assert "warning" in result