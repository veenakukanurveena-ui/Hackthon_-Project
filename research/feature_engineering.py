import pandas as pd
import numpy as np


def prepare_features(data):
    """
    Clean telemetry data and generate
    features for AI-based anomaly detection.
    """

    df = pd.DataFrame(data)

    required_columns = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "latency_ms",
        "packet_loss_pct",
        "failed_login_count"
    ]

    # Check required telemetry fields
    for column in required_columns:
        if column not in df.columns:
            df[column] = 0

    # Convert values to numeric
    for column in required_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Handle missing and invalid values
    df[required_columns] = df[required_columns].replace(
        [np.inf, -np.inf], np.nan
    )

    df[required_columns] = df[required_columns].fillna(0)

    # Keep values within valid ranges
    percentage_columns = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "packet_loss_pct"
    ]

    for column in percentage_columns:
        df[column] = df[column].clip(0, 100)

    df["latency_ms"] = df["latency_ms"].clip(lower=0)
    df["failed_login_count"] = df["failed_login_count"].clip(lower=0)

    # Generate additional AI features
    df["resource_pressure"] = (
        df["cpu_usage"] + df["memory_usage"] + df["disk_usage"]
    ) / 3

    df["network_risk"] = (
        df["latency_ms"] * (1 + df["packet_loss_pct"] / 100)
    )

    df["security_risk"] = np.log1p(
        df["failed_login_count"]
    )

    return df


if __name__ == "__main__":

    sample_data = [
        {
            "cpu_usage": 45,
            "memory_usage": 55,
            "disk_usage": 60,
            "latency_ms": 30,
            "packet_loss_pct": 0,
            "failed_login_count": 1
        },
        {
            "cpu_usage": 98,
            "memory_usage": 95,
            "disk_usage": 85,
            "latency_ms": 190,
            "packet_loss_pct": 12,
            "failed_login_count": 15
        }
    ]

    result = prepare_features(sample_data)

    print("\nPrepared AI Features:")
    print(result.to_string(index=False))