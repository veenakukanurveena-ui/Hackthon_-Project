import psutil
import platform
from datetime import datetime


def collect_system_metrics():

    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get RAM usage
    memory = psutil.virtual_memory()
    ram_usage = memory.percent

    # Get disk usage
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    # Prepare collected information
    metrics = {
        "device": platform.node(),
        "operating_system": platform.system(),
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage,
        "disk_usage_percent": disk_usage,
        "timestamp": datetime.now().isoformat()
    }

    return metrics


if __name__ == "__main__":
    data = collect_system_metrics()
    print(data)