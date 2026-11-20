import pandas as pd
from research.feature_engineering import prepare_features


def test_prepare_features_creates_derived_columns():
    data = {
        "cpu_usage": [80],
        "memory_usage": [70],
        "disk_usage": [60],
        "latency_ms": [100],
        "packet_loss_pct": [2],
        "failed_login_count": [3]
    }

    result = prepare_features(data)

    assert "resource_pressure" in result.columns
    assert "network_risk" in result.columns
    assert "security_risk" in result.columns


def test_prepare_features_handles_missing_values():
    data = {
        "cpu_usage": [None],
        "memory_usage": [70],
        "disk_usage": [60],
        "latency_ms": [100],
        "packet_loss_pct": [2],
        "failed_login_count": [3]
    }

    result = prepare_features(data)

    assert not result.isnull().values.any()