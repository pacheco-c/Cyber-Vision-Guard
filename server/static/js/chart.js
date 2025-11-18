document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("eventChart");

  const labels = window.eventLabels;       // ID evento
  const durations = window.eventDurations; // Durata
  const tooltipInfo = window.eventTooltips; // Info extra per tooltip

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Durata evento (s)",
          data: durations,
          backgroundColor: "rgba(0, 200, 255, 0.4)",
          borderColor: "rgb(0, 200, 255)",
          borderWidth: 2,
          borderRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              const idx = context.dataIndex;
              const info = tooltipInfo[idx] || "";
              return `Durata: ${context.parsed.y}s — ${info}`;
            },
          },
        },
      },
      scales: {
        x: {
          title: { display: true, text: "ID Evento" },
        },
        y: {
          title: { display: true, text: "Durata (s)" },
          beginAtZero: true,
        },
      },
    },
  });
});