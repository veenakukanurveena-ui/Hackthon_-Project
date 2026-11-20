import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "sentinelops.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                host_id TEXT NOT NULL,
                service TEXT NOT NULL,
                severity TEXT NOT NULL,
                event_type TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                anomaly_score REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(timestamp, host_id, service, event_type)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS security_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        """)


def save_telemetry(data):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT OR IGNORE INTO telemetry (
                timestamp, host_id, service, severity,
                event_type, metric, value, unit, anomaly_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["timestamp"],
            data["host_id"],
            data["service"],
            data["severity"],
            data["event_type"],
            data["metric"],
            data["value"],
            data["unit"],
            data["anomaly_score"]
        ))
        return cursor.rowcount == 1


def get_all_telemetry():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM telemetry ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def save_audit(event_type, reason):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO security_audit (event_type, reason)
            VALUES (?, ?)
        """, (event_type, reason))