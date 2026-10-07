/*
 * Renders admin-web's 30-day user-history bar chart. Reads its JSON from the element whose id
 * is in `data-user-history`, and dataset/empty labels from data-* attributes (localized
 * server-side). No-ops (showing the empty note) when Chart.js is absent or the history is empty.
 */
(function () {
  var container = document.querySelector(".metrics-chart[data-user-history]");
  if (!container) {
    return;
  }
  var canvas = container.querySelector("canvas");
  var empty = container.querySelector(".metrics-chart-empty");
  var raw = document.getElementById(container.getAttribute("data-user-history"));

  var data = [];
  try {
    data = JSON.parse((raw && raw.textContent) || "[]");
  } catch (e) {
    data = [];
  }

  if (!window.Chart || !Array.isArray(data) || data.length === 0) {
    if (canvas) {
      canvas.hidden = true;
    }
    if (empty) {
      empty.hidden = false;
    }
    return;
  }

  var accent = (
    getComputedStyle(document.documentElement).getPropertyValue("--color-accent") || "#7c93ff"
  ).trim();

  new window.Chart(canvas, {
    type: "bar",
    data: {
      labels: data.map(function (d) {
        return d.date;
      }),
      datasets: [
        {
          label: container.getAttribute("data-label-total"),
          data: data.map(function (d) {
            return d.total_users;
          }),
          backgroundColor: accent,
        },
        {
          label: container.getAttribute("data-label-new"),
          data: data.map(function (d) {
            return d.new_users;
          }),
          backgroundColor: accent.indexOf("#") === 0 ? accent + "66" : accent,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom" },
        tooltip: { mode: "index", intersect: false },
      },
      scales: {
        x: { ticks: { maxRotation: 0, autoSkip: true } },
        y: { beginAtZero: true, ticks: { precision: 0 } },
      },
    },
  });
})();
