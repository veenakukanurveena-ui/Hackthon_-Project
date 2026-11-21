// SentinelOps - Dashboard Data

document.addEventListener("DOMContentLoaded", async function () {

  console.log("Loading SentinelOps dashboard...");

  // Check backend connection
  if (typeof checkBackendHealth === "function") {

      const health = await checkBackendHealth();

      console.log("Backend status:", health);

      const statusElement = document.getElementById("backend-status");

      if (statusElement) {
          if (health.success === true || health.status === "ok") {
              statusElement.textContent = "Backend Connected";
              statusElement.classList.add("good");
          } else {
              statusElement.textContent = "Backend Offline";
              statusElement.classList.add("bad");
          }
      }
  }

  // Load telemetry data
  if (typeof getTelemetry === "function") {

      const telemetry = await getTelemetry();

      console.log("Telemetry received:", telemetry);

      updateTelemetryDisplay(telemetry);
  }

});

// Update telemetry display
function updateTelemetryDisplay(data) {

  if (!data) {
      console.log("No telemetry data available.");
      return;
  }

  const telemetryList = Array.isArray(data)
      ? data
      : (data.data || data.telemetry || []);

  console.log("Telemetry records:", telemetryList.length);

  const countElement = document.getElementById("telemetry-count");

  if (countElement) {
      countElement.textContent = telemetryList.length;
  }
}