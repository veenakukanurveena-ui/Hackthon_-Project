from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    initialize_database,
    save_telemetry,
    get_all_telemetry,
    save_audit
)

from validator import validate_telemetry
from detector import detect_anomaly

app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# Initialize database
initialize_database()


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "SentinelOps",
        "message": "Privacy-First AIOps Backend is running",
        "status": "online"
    })


# Health check
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "SentinelOps Backend",
        "database": "connected"
    })


# Receive telemetry
@app.route("/api/telemetry", methods=["POST"])
def receive_telemetry():

    if not request.is_json:
        save_audit("REJECTED", "Request was not JSON")
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 415

    data = request.get_json(silent=True)

    valid, message, safe_data = validate_telemetry(data)

    if not valid:
        save_audit("REJECTED", message)
        return jsonify({
            "success": False,
            "message": message,
            "security": "Payload rejected"
        }), 400

    inserted = save_telemetry(safe_data)

    if not inserted:
        return jsonify({
            "success": True,
            "message": "Duplicate event ignored",
            "stored": False
        }), 200

    return jsonify({
        "success": True,
        "message": "Safe telemetry received and stored",
        "stored": True
    }), 201


# Retrieve telemetry and analyze anomalies
@app.route("/api/telemetry", methods=["GET"])
def retrieve_telemetry():

    records = get_all_telemetry()

    for record in records:
        record["analysis"] = detect_anomaly(record)

    return jsonify({
        "success": True,
        "count": len(records),
        "data": records
    })


# Handle oversized requests
@app.errorhandler(413)
def request_too_large(error):
    return jsonify({
        "success": False,
        "error": "Request exceeds allowed size"
    }), 413


# Start Flask server
if __name__ == "__main__":
    print("Starting SentinelOps Backend...")
    app.run(host="127.0.0.1", port=5000, debug=False)