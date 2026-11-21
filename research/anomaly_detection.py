import pandas as pd

from research.model_training import AnomalyModelTrainer


class AnomalyDetectionEngine:

    def __init__(self):
        self.trainer = AnomalyModelTrainer()
        self.is_trained = False

    def train_detector(self, training_data):
        """
        Train the anomaly detection model.
        """

        self.trainer.train(training_data)
        self.is_trained = True

    def classify_severity(self, telemetry):
        """
        Classify anomaly severity using telemetry thresholds.
        """

        critical_conditions = [
            telemetry.get("cpu_usage", 0) >= 95,
            telemetry.get("memory_usage", 0) >= 95,
            telemetry.get("disk_usage", 0) >= 95,
            telemetry.get("latency_ms", 0) >= 250,
            telemetry.get("packet_loss_pct", 0) >= 15,
            telemetry.get("failed_login_count", 0) >= 20
        ]

        high_conditions = [
            telemetry.get("cpu_usage", 0) >= 90,
            telemetry.get("memory_usage", 0) >= 90,
            telemetry.get("disk_usage", 0) >= 90,
            telemetry.get("latency_ms", 0) >= 150,
            telemetry.get("packet_loss_pct", 0) >= 5,
            telemetry.get("failed_login_count", 0) >= 10
        ]

        medium_conditions = [
            telemetry.get("cpu_usage", 0) >= 75,
            telemetry.get("memory_usage", 0) >= 75,
            telemetry.get("disk_usage", 0) >= 75,
            telemetry.get("latency_ms", 0) >= 100,
            telemetry.get("packet_loss_pct", 0) >= 2,
            telemetry.get("failed_login_count", 0) >= 5
        ]

        if any(critical_conditions):
            return "Critical"

        if any(high_conditions):
            return "High"

        if any(medium_conditions):
            return "Medium"

        return "Normal"

    def detect(self, telemetry_data):
        """
        Detect anomalies and assign severity levels.
        """

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before anomaly detection."
            )

        predictions = self.trainer.predict(telemetry_data)

        results = []

        for index, prediction in enumerate(predictions):

            if isinstance(telemetry_data, pd.DataFrame):
                telemetry = telemetry_data.iloc[index].to_dict()
            else:
                telemetry = telemetry_data[index]

            severity = self.classify_severity(telemetry)

            is_anomaly = (
                prediction == "Anomaly"
                or severity != "Normal"
            )

            results.append({
                "record_id": index + 1,
                "status": "Anomaly" if is_anomaly else "Normal",
                "is_anomaly": is_anomaly,
                "severity": severity
            })

        return results


if __name__ == "__main__":

    training_data = pd.DataFrame([
        {
            "cpu_usage": 30 + i,
            "memory_usage": 35 + i,
            "disk_usage": 40 + i,
            "latency_ms": 20 + i,
            "packet_loss_pct": 1,
            "failed_login_count": 0
        }
        for i in range(20)
    ])

    engine = AnomalyDetectionEngine()

    engine.train_detector(training_data)

    test_data = pd.DataFrame([
        {
            "cpu_usage": 98,
            "memory_usage": 96,
            "disk_usage": 60,
            "latency_ms": 280,
            "packet_loss_pct": 16,
            "failed_login_count": 25
        }
    ])

    print(engine.detect(test_data))