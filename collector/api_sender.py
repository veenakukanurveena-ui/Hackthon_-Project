import requests
from telemetry_adapter import convert_to_telemetry
from system_metrics import collect_system_metrics

API_URL = "http://127.0.0.1:5000/api/telemetry"

def send_metrics():
    metrics = collect_system_metrics()
    events = convert_to_telemetry(metrics)

    for event in events:
        try:
            response = requests.post(
                API_URL,
                json=event,
                timeout=10
            )
            print("Status:", response.status_code)
            print("Response:", response.text)

        except requests.exceptions.RequestException as error:
            print("Sending failed:", error)

if __name__ == "__main__":
    send_metrics()