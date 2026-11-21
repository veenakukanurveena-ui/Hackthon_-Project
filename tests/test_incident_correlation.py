from research.incident_correlation import IncidentCorrelationEngine


def test_correlates_events_from_same_server():
    engine = IncidentCorrelationEngine(window_minutes=5)

    events = [
        {
            "server_id": "server-01",
            "timestamp": "2026-11-20 10:00:00",
            "severity": "High",
            "event_type": "CPU"
        },
        {
            "server_id": "server-01",
            "timestamp": "2026-11-20 10:02:00",
            "severity": "Critical",
            "event_type": "Memory"
        }
    ]

    incidents = engine.correlate(events)

    assert len(incidents) == 1
    assert incidents[0]["server_id"] == "server-01"
    assert incidents[0]["event_count"] == 2


def test_does_not_correlate_events_from_different_servers():
    engine = IncidentCorrelationEngine(window_minutes=5)

    events = [
        {
            "server_id": "server-01",
            "timestamp": "2026-11-20 10:00:00",
            "severity": "High",
            "event_type": "CPU"
        },
        {
            "server_id": "server-02",
            "timestamp": "2026-11-20 10:02:00",
            "severity": "High",
            "event_type": "Memory"
        }
    ]

    incidents = engine.correlate(events)

    assert len(incidents) == 0