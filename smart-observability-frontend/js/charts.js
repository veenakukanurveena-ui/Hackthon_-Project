let performanceChart = null;

function initializePerformanceChart() {

    const canvas = document.getElementById("performanceChart");

    if (!canvas || !window.Chart) {
        console.error("Chart canvas or Chart.js not found.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const purpleGradient = ctx.createLinearGradient(0, 0, 0, 300);
    purpleGradient.addColorStop(0, "rgba(155, 123, 255, 0.35)");
    purpleGradient.addColorStop(1, "rgba(155, 123, 255, 0.00)");

    const cyanGradient = ctx.createLinearGradient(0, 0, 0, 300);
    cyanGradient.addColorStop(0, "rgba(56, 229, 244, 0.24)");
    cyanGradient.addColorStop(1, "rgba(56, 229, 244, 0.00)");

    performanceChart = new Chart(ctx, {
        type: "line",

        data: {
            labels: [
                "00:00", "02:00", "04:00",
                "06:00", "08:00", "10:00",
                "12:00", "14:00", "16:00",
                "18:00", "20:00", "22:00"
            ],

            datasets: [
                {
                    label: "CPU Usage",
                    data: [42, 48, 44, 56, 51, 67, 61, 72, 65, 70, 59, 65],

                    borderColor: "#a78bfa",
                    backgroundColor: purpleGradient,

                    borderWidth: 3,
                    fill: true,
                    tension: 0.45,

                    pointRadius: 3,
                    pointHoverRadius: 7,
                    pointBackgroundColor: "#a78bfa",
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 1
                },

                {
                    label: "Memory Usage",
                    data: [55, 58, 57, 62, 64, 68, 66, 70, 73, 69, 71, 72],

                    borderColor: "#38e5f4",
                    backgroundColor: cyanGradient,

                    borderWidth: 3,
                    fill: true,
                    tension: 0.45,

                    pointRadius: 3,
                    pointHoverRadius: 7,
                    pointBackgroundColor: "#38e5f4",
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 1
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            interaction: {
                intersect: false,
                mode: "index"
            },

            animation: {
                duration: 1200,
                easing: "easeOutQuart"
            },

            plugins: {
                legend: {
                    display: false
                },

                tooltip: {
                    backgroundColor: "#111a30",
                    titleColor: "#ffffff",
                    bodyColor: "#cbd5e1",

                    borderColor: "rgba(155,123,255,.5)",
                    borderWidth: 1,

                    padding: 13,
                    cornerRadius: 10,

                    displayColors: true
                }
            },

            scales: {
                x: {
                    grid: {
                        color: "rgba(255,255,255,.045)",
                        drawBorder: false
                    },

                    ticks: {
                        color: "#8392ad",
                        font: {
                            size: 10
                        }
                    },

                    border: {
                        display: false
                    }
                },

                y: {
                    min: 0,
                    max: 100,

                    grid: {
                        color: "rgba(255,255,255,.055)",
                        drawBorder: false
                    },

                    ticks: {
                        color: "#8392ad",
                        font: {
                            size: 10
                        },

                        callback: value => value + "%"
                    },

                    border: {
                        display: false
                    }
                }
            }
        }
    });

    console.log("SentinelOps performance chart initialized.");
}


function refreshPerformanceChart() {

    if (!performanceChart) {
        initializePerformanceChart();
        return;
    }

    performanceChart.data.datasets.forEach(dataset => {

        const previousValue =
            dataset.data[dataset.data.length - 1];

        const newValue = Math.max(
            10,
            Math.min(
                95,
                previousValue + (Math.random() * 16 - 8)
            )
        );

        dataset.data.shift();
        dataset.data.push(Math.round(newValue));
    });

    performanceChart.update();
}


window.SentinelCharts = {
    initializePerformanceChart,
    refreshPerformanceChart
};


// Initialize after HTML loads
document.addEventListener("DOMContentLoaded", () => {
    initializePerformanceChart();
});