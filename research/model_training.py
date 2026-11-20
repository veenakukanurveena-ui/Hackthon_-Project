import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class AnomalyModelTrainer:

    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.scaler = StandardScaler()

        self.model = IsolationForest(
            n_estimators=200,
            contamination=self.contamination,
            random_state=self.random_state,
            max_samples="auto"
        )

    def train(self, data):

        if data.empty:
            raise ValueError("Training data cannot be empty.")

        if data.isnull().values.any():
            raise ValueError("Training data contains missing values.")

        self.scaler.fit(data)
        scaled_data = self.scaler.transform(data)

        self.model.fit(scaled_data)

        print("AI anomaly detection model trained successfully.")

    def predict(self, data):

        if not hasattr(self.model, "estimators_"):
            raise RuntimeError("Train the model before prediction.")

        scaled_data = self.scaler.transform(data)

        predictions = self.model.predict(scaled_data)

        return [
            "Normal" if value == 1 else "Anomaly"
            for value in predictions
        ]

    def save_model(self, path="models/anomaly_model.pkl"):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        joblib.dump({
            "model": self.model,
            "scaler": self.scaler
        }, path)

        print(f"Model saved successfully: {path}")


if __name__ == "__main__":

    # Sample telemetry for demonstration
    training_data = pd.DataFrame({
        "cpu_usage": [35, 40, 42, 38, 45, 41, 39, 43],
        "memory_usage": [50, 52, 48, 55, 51, 49, 53, 50],
        "disk_usage": [60, 62, 61, 59, 63, 60, 58, 61],
        "latency_ms": [25, 28, 30, 26, 29, 27, 24, 28],
        "packet_loss_pct": [0, 0, 1, 0, 0, 0, 0, 1],
        "failed_login_count": [0, 1, 0, 0, 1, 0, 0, 1]
    })

    trainer = AnomalyModelTrainer()

    trainer.train(training_data)

    test_data = pd.DataFrame({
        "cpu_usage": [40, 98],
        "memory_usage": [50, 95],
        "disk_usage": [60, 90],
        "latency_ms": [28, 200],
        "packet_loss_pct": [0, 15],
        "failed_login_count": [0, 20]
    })

    results = trainer.predict(test_data)

    print("\nAnomaly Detection Results:")

    for index, result in enumerate(results):
        print(f"Sample {index + 1}: {result}")

    trainer.save_model()