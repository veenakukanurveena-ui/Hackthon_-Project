import pandas as pd

from research.feature_engineering import prepare_features
from research.anomaly_detection import AnomalyDetectionEngine
from research.incident_correlation import IncidentCorrelationEngine
from research.root_cause import RootCauseAnalyzer
from research.recommendations import RecommendationEngine
from research.model_explanation import ModelExplainer


class AIPipeline:

    def __init__(self):
        self.detector = AnomalyDetectionEngine()
        self.incident_engine = IncidentCorrelationEngine()
        self.root_cause = RootCauseAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.explainer = ModelExplainer()

        self.is_trained = False

    def train(self, training_telemetry):
        """
        Train the anomaly detection model using approved telemetry.
        """

        training_df = pd.DataFrame(training_telemetry)

        features = prepare_features(training_df)

        self.detector.train_detector(features)

        self.is_trained = True

        return {
            "status": "success",
            "message": "AI anomaly detection model trained successfully.",
            "training_records": len(features)
        }

    def analyze(self, telemetry_records):
        """
        Analyze approved telemetry and generate AI-assisted insights.
        """

        if not self.is_trained:
            raise RuntimeError(
                "Train the AI pipeline before analyzing telemetry."
            )

        telemetry_df = pd.DataFrame(telemetry_records)

        features = prepare_features(telemetry_df)

        # Remove metadata columns before ML prediction
        features = features.drop(
            columns=["host_id", "server_id", "service", "timestamp"],
            errors="ignore"
        )

        predictions = self.detector.detect(features)

        results = []
        incident_events = []

        for index, prediction in enumerate(predictions):

            original_data = telemetry_df.iloc[index].to_dict()
            feature_data = features.iloc[index].to_dict()

            combined_data = {
                **original_data,
                **feature_data
            }

            explanation = self.explainer.explain(
                combined_data,
                prediction["status"]
            )

            result = {
                "record_id": index + 1,
                "anomaly_status": prediction["status"],
                "is_anomaly": prediction["is_anomaly"],
                "explanation": explanation,
                "root_cause_analysis": None,
                "recommendations": []
            }

            if prediction["is_anomaly"]:

                result["root_cause_analysis"] = (
                    self.root_cause.analyze(combined_data)
                )

                result["recommendations"] = (
                    self.recommendation_engine.generate(combined_data)
                )

                if (
                    combined_data.get("server_id")
                    and combined_data.get("timestamp")
                ):
                    incident_events.append({
                        "server_id": combined_data["server_id"],
                        "timestamp": combined_data["timestamp"],
                        "severity": "High",
                        "event_type": "Telemetry anomaly"
                    })

            results.append(result)

        incidents = self.incident_engine.correlate(incident_events)

        return {
            "status": "success",
            "total_records": len(telemetry_df),
            "anomalies_detected": sum(
                item["is_anomaly"] for item in results
            ),
            "results": results,
            "correlated_incidents": incidents
        }