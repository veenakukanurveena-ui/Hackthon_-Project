const API_URL = "http://10.82.18.17:5000";

// Get HTML elements
const totalRecords = document.getElementById("totalRecords");
const healthyRecords = document.getElementById("healthyRecords");
const anomalyRecords = document.getElementById("anomalyRecords");
const backendStatus = document.getElementById("backendStatus");
const connectionStatus = document.getElementById("connectionStatus");

const cpuValue = document.getElementById("cpuValue");
const ramValue = document.getElementById("ramValue");
const diskValue = document.getElementById("diskValue");

const telemetryTable = document.getElementById("telemetryTable");
const alertsList = document.getElementById("alertsList");

// Update metric display
function updateMetric(valueElement, barElement, value) {
    const safeValue = Math.max(0, Math.min(100, Number(value)));

    valueElement.textContent = safeValue.toFixed(1) + "%";
    barElement.style.width = safeValue + "%";

    barElement.style.background =
        safeValue >= 90 ? "#ef4444" :
        safeValue >= 80 ? "#f59e0b" : "#22c55e";
}

// Check backend connection
async function checkBackend() {
    try {
        const response = await fetch(`${API_URL}/api/health`);

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        const result = await response.json();

        backendStatus.textContent = result.status === "healthy"
            ? "Online" : "Unavailable";

        connectionStatus.textContent = result.status === "healthy"
            ? "Connected" : "Unavailable";

    } catch (error) {
        backendStatus.textContent = "Offline";
        connectionStatus.textContent = "Disconnected";
        console.error("Backend connection error:", error);
    }
}

// Fetch telemetry records
async function loadTelemetry() {
    try {
        const response = await fetch(`${API_URL}/api/telemetry`);

        if (!response.ok) {
            throw new Error("Unable to fetch telemetry");
        }

        const result = await response.json();
        const records = result.data || [];

        totalRecords.textContent = records.length;

        const anomalies = records.filter(record =>
            record.analysis &&
            record.analysis.is_anomaly
        );

        const healthy = records.length - anomalies.length;

        healthyRecords.textContent = healthy;
        anomalyRecords.textContent = anomalies.length;

        displayMetrics(records);
        displayAlerts(records);
        displayTable(records);

    } catch (error) {
        console.error("Telemetry error:", error);
        alertsList.textContent = "Unable to load telemetry. Check backend connection.";
        telemetryTable.innerHTML =
            '<tr><td colspan="5">Backend data unavailable</td></tr>';
    }
}

// Display latest CPU, RAM and disk values
function displayMetrics(records) {
    const latest = {};

    records.forEach(record => {
        if (!latest[record.metric]) {
            latest[record.metric] = record;
        }
    });

    if (latest.cpu_usage) {
        updateMetric(cpuValue, document.getElementById("cpuBar"),
            latest.cpu_usage.value);
    }

    if (latest.memory_usage) {
        updateMetric(ramValue, document.getElementById("ramBar"),
            latest.memory_usage.value);
    }

    if (latest.disk_usage) {
        updateMetric(diskValue, document.getElementById("diskBar"),
            latest.disk_usage.value);
    }
}

// Display anomaly alerts
function displayAlerts(records) {
    const alerts = [];

    records.forEach(record => {
        const analysis = record.analysis;

        if (analysis && analysis.is_anomaly) {
            alerts.push({
                metric: record.metric,
                value: record.value,
                risk: analysis.risk_level,
                reasons: analysis.explanation || []
            });
        }
    });

    if (alerts.length === 0) {
        alertsList.innerHTML =
            '<div class="alert-item normal">No anomalies detected in available records.</div>';
        return;
    }

    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.risk === "CRITICAL" ? "critical" : ""}">
            <strong>${escapeHTML(alert.risk)}</strong> -
            ${escapeHTML(alert.metric)}: ${escapeHTML(alert.value)}<br>
            ${alert.reasons.map(reason => escapeHTML(reason)).join("<br>")}
        </div>
    `).join("");
}

// Prevent untrusted text from being interpreted as HTML
function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

// Display telemetry table
function displayTable(records) {
    if (records.length === 0) {
        telemetryTable.innerHTML =
            '<tr><td colspan="5">No telemetry records received yet.</td></tr>';
        return;
    }

    telemetryTable.innerHTML = records.map(record => {
        const risk = record.analysis
            ? record.analysis.risk_level : "LOW";

        return `
            <tr>
                <td>${escapeHTML(record.host_id)}</td>
                <td>${escapeHTML(record.metric)}</td>
                <td>${escapeHTML(record.value)} ${escapeHTML(record.unit)}</td>
                <td>${escapeHTML(record.severity)}</td>
                <td class="risk ${escapeHTML(risk)}">${escapeHTML(risk)}</td>
            </tr>
        `;
    }).join("");
}

// Refresh dashboard
async function refreshDashboard() {
    await checkBackend();
    await loadTelemetry();
}

document.getElementById("refreshBtn")
    .addEventListener("click", refreshDashboard);

// Initial load and automatic refresh every 10 seconds
refreshDashboard();
setInterval(refreshDashboard, 10000);