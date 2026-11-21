// SentinelOps - Dashboard Charts

document.addEventListener("DOMContentLoaded", function () {

  // Check whether Chart.js is available
  if (typeof Chart === "undefined") {
      console.log("Chart.js is not loaded yet.");
      return;
  }

  const chartCanvas = document.getElementById("telemetryChart");

  if (!chartCanvas) {
      console.log("Telemetry chart canvas not found.");
      return;
  }

  new Chart(chartCanvas, {
      type: "line",

      data: {
          labels: [
              "10:00",
              "10:05",
              "10:10",
              "10:15",
              "10:20",
              "10:25"
          ],

          datasets: [
              {
                  label: "CPU Usage (%)",
                  data: [35, 42, 38, 65, 52, 45],
                  borderColor: "#8b7cff",
                  backgroundColor: "rgba(139, 124, 255, 0.12)",
                  fill: true,
                  tension: 0.4
              },
              {
                  label: "Memory Usage (%)",
                  data: [45, 48, 51, 49, 55, 53],
                  borderColor: "#36c9e8",
                  backgroundColor: "rgba(54, 201, 232, 0.08)",
                  fill: true,
                  tension: 0.4
              }
          ]
      },

      options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
              legend: {
                  labels: {
                      color: "#edf3ff"
                  }
              }
          },

          scales: {
              x: {
                  ticks: {
                      color: "#91a0b8"
                  },
                  grid: {
                      color: "#24334a"
                  }
              },

              y: {
                  beginAtZero: true,
                  max: 100,
                  ticks: {
                      color: "#91a0b8"
                  },
                  grid: {
                      color: "#24334a"
                  }
              }
          }
      }
  });

});