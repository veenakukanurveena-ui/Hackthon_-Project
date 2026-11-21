const API_BASE_URL = "http://127.0.0.1:5000";

async function apiRequest(endpoint, options = {}) {
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

    return response.json();
}

async function checkBackendHealth() {
    return apiRequest("/api/health");
}

window.SentinelAPI = {
    apiRequest,
    checkBackendHealth
};