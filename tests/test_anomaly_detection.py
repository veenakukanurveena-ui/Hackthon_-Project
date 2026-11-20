import pandas as pd
import pytest

from research.anomaly_detection import AnomalyDetectionEngine


def get_training_data():
    return pd.DataFrame({
        "cpu_usage": [20, 25, 30, 35, 40, 45, 50, 55],
        "memory_usage": [30, 35, 40, 45, 50, 55, 60, 65],
        "disk_usage": [20, 25, 30, 35, 40, 45, 50, 55],
        "latency_ms": [20, 25, 30, 35, 40, 45, 50, 55],
        "packet_loss_pct": [0, 0, 1, 0, 1, 0, 1, 0],
        "failed_login_count": [0, 1, 0, 1, 0, 1, 0, 1]
    })


def test_detection_requires_training():
    engine = AnomalyDetectionEngine()

    with pytest.raises(RuntimeError):
        engine.detect(get_training_data())


def test_detection_returns_valid_results():
    engine = AnomalyDetectionEngine()
    training_data = get_training_data()

    engine.train_detector(training_data)
    results = engine.detect(training_data)

    assert len(results) == len(training_data)

    for result in results:
        assert "record_id" in result
        assert "status" in result
        assert "is_anomaly" in result
        assert result["status"] in ["Normal", "Anomaly"]
        assert isinstance(result["is_anomaly"], bool)