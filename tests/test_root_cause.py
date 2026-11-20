from research.root_cause import RootCauseAnalyzer


def test_detects_high_cpu_usage():
    analyzer = RootCauseAnalyzer()

    telemetry = {
        "cpu_usage": 95,
        "memory_usage": 60,
        "disk_usage": 50,
        "latency_ms": 40,
        "packet_loss_pct": 0,
        "failed_logins": 0
    }

    result = analyzer.analyze(telemetry)

    assert "possible_contributing_factors" in result
    assert len(result["possible_contributing_factors"]) > 0


def test_returns_investigation_recommendations():
    analyzer = RootCauseAnalyzer()

    telemetry = {
        "cpu_usage": 95,
        "memory_usage": 92,
        "disk_usage": 50,
        "latency_ms": 180,
        "packet_loss_pct": 6,
        "failed_logins": 0
    }

    result = analyzer.analyze(telemetry)

    assert "recommended_investigations" in result
    assert len(result["recommended_investigations"]) > 0