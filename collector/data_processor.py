import json
from system_metrics import collect_system_metrics


def save_metrics():

    # Collect system information
    metrics = collect_system_metrics()

    # Save information in JSON format
    with open("metrics.json", "w") as file:
        json.dump(metrics, file, indent=4)

    print("System metrics saved successfully!")
    print(metrics)


if __name__ == "__main__":
    save_metrics()