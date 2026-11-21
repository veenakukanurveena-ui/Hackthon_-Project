from datetime import datetime


class IncidentCorrelationEngine:

    def __init__(self, window_minutes=5):
        self.window_minutes = window_minutes

    def get_priority(self, events):
        """
        Determine incident priority from the highest event severity.
        """

        priority_order = {
            "Critical": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        highest_priority = max(
            (
                priority_order.get(
                    event.get("severity", "Low"),
                    1
                )
                for event in events
            ),
            default=1
        )

        for priority, value in priority_order.items():
            if value == highest_priority:
                return priority

        return "Low"

    def parse_timestamp(self, timestamp):
        """
        Convert timestamp strings into datetime objects.
        """

        if isinstance(timestamp, datetime):
            return timestamp

        return datetime.fromisoformat(
            str(timestamp).replace("Z", "+00:00")
        )

    def correlate(self, events):
        """
        Group related events from the same server
        within the configured time window.
        """

        if not events:
            return []

        valid_events = []

        for event in events:
            if not event.get("server_id") or not event.get("timestamp"):
                continue

            normalized_event = event.copy()
            normalized_event["_parsed_time"] = self.parse_timestamp(
                event["timestamp"]
            )

            valid_events.append(normalized_event)

        valid_events.sort(
            key=lambda event: event["_parsed_time"]
        )

        server_groups = {}

        for event in valid_events:
            server_id = event["server_id"]
            server_groups.setdefault(server_id, []).append(event)

        incidents = []

        for server_id, server_events in server_groups.items():

            current_group = []

            for event in server_events:

                if not current_group:
                    current_group.append(event)
                    continue

                previous_time = current_group[-1]["_parsed_time"]
                current_time = event["_parsed_time"]

                time_difference = (
                    current_time - previous_time
                ).total_seconds() / 60

                if time_difference <= self.window_minutes:
                    current_group.append(event)

                else:
                    self._create_incident(
                        current_group,
                        server_id,
                        incidents
                    )

                    current_group = [event]

            if current_group:
                self._create_incident(
                    current_group,
                    server_id,
                    incidents
                )

        return incidents

    def _create_incident(self, events, server_id, incidents):
        """
        Create an incident from a correlated event group.
        """

        if len(events) < 2:
            return

        clean_events = []

        for event in events:
            clean_event = {
                key: value
                for key, value in event.items()
                if key != "_parsed_time"
            }
            clean_events.append(clean_event)

        incidents.append({
            "incident_id": f"INC-{len(incidents) + 1:04d}",
            "incident_type": "Correlated infrastructure anomaly",
            "server_id": server_id,
            "priority": self.get_priority(clean_events),
            "event_count": len(clean_events),
            "related_events": clean_events,
            "first_seen": str(events[0]["timestamp"]),
            "last_seen": str(events[-1]["timestamp"]),
            "status": "Open"
        })


if __name__ == "__main__":

    sample_events = [
        {
            "server_id": "SERVER-01",
            "timestamp": "2026-11-20T10:00:00",
            "severity": "High",
            "event_type": "CPU usage anomaly"
        },
        {
            "server_id": "SERVER-01",
            "timestamp": "2026-11-20T10:02:00",
            "severity": "Critical",
            "event_type": "Memory usage anomaly"
        },
        {
            "server_id": "SERVER-01",
            "timestamp": "2026-11-20T10:04:00",
            "severity": "Medium",
            "event_type": "Network latency anomaly"
        }
    ]

    engine = IncidentCorrelationEngine(window_minutes=5)

    incidents = engine.correlate(sample_events)

    for incident in incidents:
        print(incident)