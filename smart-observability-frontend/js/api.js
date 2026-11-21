const API_BASE_URL = "http://127.0.0.1:5000";

// CENTRAL API REQUEST FUNCTION
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("SentinelOps API Error:", error);
        throw error;
    }
}

// CHECK BACKEND CONNECTION
async function checkBackendHealth() {
    return apiRequest("/api/health");
}

// GET TELEMETRY
async function getTelemetry() {
    return apiRequest("/api/telemetry");
}

// SEND TELEMETRY
async function sendTelemetry(data) {
    return apiRequest("/api/telemetry", {
        method: "POST",
        body: JSON.stringify(data)
    });
}

// MAKE FUNCTIONS AVAILABLE TO OTHER FRONTEND FILES
window.SentinelAPI = {
    apiRequest,
    checkBackendHealth,
    getTelemetry,
    sendTelemetry
};