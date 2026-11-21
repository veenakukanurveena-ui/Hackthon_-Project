from research.ai_pipeline import AIPipeline


class BackendAIIntegration:

    METRIC_FIELDS = {
        "cpu_usage": "cpu_usage",
        "memory_usage": "memory_usage",
        "disk_usage": "disk_usage",
        "latency_ms": "latency_ms",
        "packet_loss_pct": "packet_loss_pct",
        "failed_login_count": "failed_login_count"
    }

    def __init__(self):
        self.pipeline = AIPipeline()
        self.is_trained = False

    def train(self, training_data):
        self.pipeline.train(training_data)
        self.is_trained = True
        return {"success": True, "message": "AI model trained"}

    def convert_backend_records(self, records):
        grouped = {}

        for record in records:
            key = (
                record.get("timestamp"),
                record.get("host_id"),
                record.get("service")
            )

            if key not in grouped:
                grouped[key] = {
                    "timestamp": record.get("timestamp"),
                    "server_id": record.get("host_id"),
                    "host_id": record.get("host_id"),
                    "service": record.get("service"),
                    "cpu_usage": 0,
                    "memory_usage": 0,
                    "disk_usage": 0,
                    "latency_ms": 0,
                    "packet_loss_pct": 0,
                    "failed_login_count": 0
                }

            metric = record.get("metric", "").lower()
            field = self.METRIC_FIELDS.get(metric)

            if field:
                grouped[key][field] = record.get("value", 0)

        return list(grouped.values())

    def analyze(self, telemetry_data):
        if not self.is_trained:
            return {
                "success": False,
                "message": "AI model is not trained yet"
            }

        combined_data = self.convert_backend_records(telemetry_data)

        return self.pipeline.analyze(combined_data)