document.addEventListener("DOMContentLoaded", () => {

  // Initialize Lucide icons
  if (window.lucide) {
      lucide.createIcons();
  }

  console.log("SentinelOps Command Center loaded.");

  // ==================================
  // MOBILE SIDEBAR
  // ==================================

  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.querySelector(".sidebar");

  if (menuToggle && sidebar) {
      menuToggle.addEventListener("click", () => {
          sidebar.classList.toggle("open");
      });
  }

  // ==================================
  // SIDEBAR NAVIGATION
  // ==================================

  const navLinks = document.querySelectorAll(".sidebar nav a");

  navLinks.forEach(link => {

      link.addEventListener("click", event => {

          event.preventDefault();

          navLinks.forEach(item => {
              item.classList.remove("active");
          });

          link.classList.add("active");

          if (sidebar) {
              sidebar.classList.remove("open");
          }

          showNotification(
              link.querySelector("span")?.textContent ||
              link.textContent.trim()
          );

      });

  });

  // ==================================
  // DASHBOARD REFRESH
  // ==================================

  const refreshButton =
      document.getElementById("refreshButton");

  if (refreshButton) {

      refreshButton.addEventListener("click", async () => {

          refreshButton.disabled = true;

          const originalContent = refreshButton.innerHTML;

          refreshButton.innerHTML =
              '<i data-lucide="loader-circle"></i><span>Refreshing...</span>';

          if (window.lucide) {
              lucide.createIcons();
          }

          // Refresh demonstration chart
          if (window.SentinelCharts) {
              window.SentinelCharts.refreshPerformanceChart();
          }

          // Check backend connection
          if (window.SentinelAPI) {
              await window.SentinelAPI.checkBackendHealth();
          }

          refreshButton.innerHTML = originalContent;
          refreshButton.disabled = false;

          if (window.lucide) {
              lucide.createIcons();
          }

          showNotification(
              "Dashboard refreshed. Demo metrics remain simulated until live telemetry is connected."
          );

      });

  }

  // ==================================
  // DASHBOARD SEARCH
  // ==================================

  const searchInput =
      document.getElementById("dashboardSearch");

  if (searchInput) {

      searchInput.addEventListener("input", () => {

          const query =
              searchInput.value.toLowerCase().trim();

          const searchableItems = document.querySelectorAll(
              ".kpi-card, .chart-container, .ai-card, .dashboard-section"
          );

          searchableItems.forEach(item => {

              const matches =
                  item.textContent.toLowerCase().includes(query);

              item.style.opacity =
                  !query || matches ? "1" : "0.18";

              item.style.filter =
                  !query || matches ? "none" : "grayscale(1)";

          });

      });

      // Clear search with Escape
      searchInput.addEventListener("keydown", event => {

          if (event.key === "Escape") {

              searchInput.value = "";
              searchInput.dispatchEvent(
                  new Event("input")
              );

          }

      });

  }

  // ==================================
  // KEYBOARD SEARCH SHORTCUT
  // ==================================

  document.addEventListener("keydown", event => {

      if (
          (event.ctrlKey || event.metaKey) &&
          event.key.toLowerCase() === "k"
      ) {

          event.preventDefault();

          if (searchInput) {
              searchInput.focus();
          }

      }

  });

  // ==================================
  // AI INSIGHTS BUTTONS
  // ==================================

  const aiButtons = [
      document.getElementById("exploreAIButton"),
      document.getElementById("exploreAIButton2")
  ];

  aiButtons.forEach(button => {

      if (button) {

          button.addEventListener("click", () => {

              showNotification(
                  "AI Intelligence selected. Connect the AI analysis service to display actual analysis results."
              );

          });

      }

  });

  // ==================================
  // RUN AI ANALYSIS
  // ==================================

  const runAnalysisButton =
      document.getElementById("runAnalysisButton");

  if (runAnalysisButton) {

      runAnalysisButton.addEventListener("click", () => {

          showNotification(
              "AI analysis requested. Live analysis will be enabled after API integration."
          );

      });

  }

  // ==================================
  // NOTIFICATIONS
  // ==================================

  const notificationButton =
      document.getElementById("notificationButton");

  if (notificationButton) {

      notificationButton.addEventListener("click", () => {

          showNotification(
              "There are 4 demonstration incidents in the dashboard."
          );

      });

  }

  // ==================================
  // REPORTS
  // ==================================

  const reportsButton =
      document.getElementById("reportsButton");

  if (reportsButton) {

      reportsButton.addEventListener("click", () => {

          showNotification(
              "Reports module selected. Report generation is not connected yet."
          );

      });

  }

  // ==================================
  // ALERT MANAGEMENT
  // ==================================

  const alertsButton =
      document.getElementById("alertsButton");

  if (alertsButton) {

      alertsButton.addEventListener("click", () => {

          showNotification(
              "Alert management selected. Alert controls will be integrated next."
          );

      });

  }

  // ==================================
  // BACKEND HEALTH CHECK
  // ==================================

  if (window.SentinelAPI) {

      window.SentinelAPI.checkBackendHealth();

  }

});


// ======================================
// PREMIUM NOTIFICATION
// ======================================

function showNotification(message) {

  const oldToast = document.querySelector(".toast");

  if (oldToast) {
      oldToast.remove();
  }

  const toast = document.createElement("div");

  toast.className = "toast";

  toast.textContent = message;

  document.body.appendChild(toast);

  setTimeout(() => {

      toast.remove();

  }, 3500);

}