from research.recommendations import RecommendationEngine


def test_generates_cpu_recommendation():
    engine = RecommendationEngine()

    telemetry = {
        "cpu_usage": 95,
        "memory_usage": 60,
        "disk_usage": 50,
        "latency_ms": 40,
        "packet_loss_pct": 0,
        "failed_login_count": 0
    }

    results = engine.generate(telemetry)

    assert len(results) > 0
    assert any(
        "cpu" in item["issue"].lower()
        for item in results
    )


def test_recommendations_require_human_approval():
    engine = RecommendationEngine()

    telemetry = {
        "cpu_usage": 95,
        "memory_usage": 92,
        "disk_usage": 50,
        "latency_ms": 180,
        "packet_loss_pct": 6,
        "failed_login_count": 15
    }

    results = engine.generate(telemetry)

    assert len(results) > 0

    for item in results:
        assert item["requires_human_approval"] is True