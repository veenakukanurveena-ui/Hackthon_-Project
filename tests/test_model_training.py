import pandas as pd
from research.model_training import AnomalyModelTrainer


def test_model_training_and_prediction():
    data = pd.DataFrame({
        "cpu_usage": [20, 25, 30, 35, 40, 45, 50, 55],
        "memory_usage": [30, 35, 40, 45, 50, 55, 60, 65],
        "disk_usage": [20, 25, 30, 35, 40, 45, 50, 55],
        "latency_ms": [20, 25, 30, 35, 40, 45, 50, 55],
        "packet_loss_pct": [0, 0, 1, 0, 1, 0, 1, 0],
        "failed_login_count": [0, 1, 0, 1, 0, 1, 0, 1]
    })

    trainer = AnomalyModelTrainer()
    trainer.train(data)

    result = trainer.predict(data)

    assert len(result) == len(data)
    assert all(value in ["Normal", "Anomaly"] for value in result)