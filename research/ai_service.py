from flask import Flask, jsonify
from flask_cors import CORS
import requests

from research.sample_telemetry import training_data
from research.backend_ai_integration import BackendAIIntegration


app = Flask(__name__)
CORS(app)

# Initialize and train the AI pipeline
ai = BackendAIIntegration()
training_result = ai.train(training_data)


@app.route("/api/ai/health", methods=["GET"])
def health():
    return jsonify({
        "service": "SentinelOps AI Service",
        "status": "online",
        "model_trained": ai.is_trained
    })


@app.route("/api/ai/analyze", methods=["GET"])
def analyze_backend_telemetry():

    try:
        # Fetch telemetry from the existing backend
        response = requests.get(
            "http://127.0.0.1:5000/api/telemetry",
            timeout=10
        )
        response.raise_for_status()

        backend_data = response.json()
        records = backend_data.get("data", [])

        if not records:
            return jsonify({
                "success": True,
                "message": "No telemetry records available",
                "results": []
            })

        # Run AI analysis
        analysis = ai.analyze(records)

        return jsonify({
            "success": True,
            "training": training_result,
            "analysis": analysis
        })

    except requests.RequestException as error:
        return jsonify({
            "success": False,
            "error": "Could not connect to the backend",
            "details": str(error)
        }), 503

    except Exception as error:
        return jsonify({
            "success": False,
            "error": "AI analysis failed",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    print("Starting SentinelOps AI Service...")
    print("AI model trained:", ai.is_trained)

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )