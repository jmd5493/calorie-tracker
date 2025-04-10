document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("progressChart");
  if (ctx) {
    const labels = JSON.parse(document.getElementById("chartLabels").textContent);
    const values = JSON.parse(document.getElementById("chartValues").textContent);

    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Calories Consumed",
          data: values,
          borderColor: "green",
          backgroundColor: "rgba(0, 255, 0, 0.1)",
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
});


