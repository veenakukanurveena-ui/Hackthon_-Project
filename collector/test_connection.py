import requests
from datetime import datetime, timezone

url = "http://10.82.18.17:5000/api/telemetry"

data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "host_id": "server-02",
    "service": "web",
    "severity": "ERROR",
    "event_type": "high_cpu",
    "metric": "cpu_usage",
    "value": 94.5,
    "unit": "percent",
    "anomaly_score": 0.92
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Backend response:", response.json())