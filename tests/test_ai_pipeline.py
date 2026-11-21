import pytest

from research.ai_pipeline import AIPipeline


def test_pipeline_requires_training():

    pipeline = AIPipeline()

    with pytest.raises(RuntimeError):
        pipeline.analyze([
            {
                "cpu_usage": 95,
                "memory_usage": 92,
                "disk_usage": 60,
                "latency_ms": 180,
                "packet_loss_pct": 8,
                "failed_login_count": 12
            }
        ])


def test_pipeline_training():

    pipeline = AIPipeline()

    training_data = [
        {
            "cpu_usage": 30 + i,
            "memory_usage": 35 + i,
            "disk_usage": 40 + i,
            "latency_ms": 20 + i,
            "packet_loss_pct": 1,
            "failed_login_count": 0
        }
        for i in range(20)
    ]

    result = pipeline.train(training_data)

    assert result["status"] == "success"
    assert result["training_records"] == 20
    assert pipeline.is_trained is True


def test_pipeline_analysis_returns_results():

    pipeline = AIPipeline()

    training_data = [
        {
            "cpu_usage": 30 + i,
            "memory_usage": 35 + i,
            "disk_usage": 40 + i,
            "latency_ms": 20 + i,
            "packet_loss_pct": 1,
            "failed_login_count": 0
        }
        for i in range(20)
    ]

    pipeline.train(training_data)

    telemetry = [
        {
            "cpu_usage": 95,
            "memory_usage": 92,
            "disk_usage": 60,
            "latency_ms": 180,
            "packet_loss_pct": 8,
            "failed_login_count": 12
        }
    ]

    result = pipeline.analyze(telemetry)

    assert result["status"] == "success"
    assert result["total_records"] == 1
    assert len(result["results"]) == 1
    assert "correlated_incidents" in result