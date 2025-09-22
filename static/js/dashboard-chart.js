document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("loginPieChart").getContext("2d");

  const chartElement = document.getElementById("loginPieChart");
  const chartLabels = JSON.parse(chartElement.dataset.labels);
  const chartData = JSON.parse(chartElement.dataset.data);

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: chartLabels,
      datasets: [
        {
          label: "Logins",
          data: chartData,
          backgroundColor: [
            "rgba(90, 50, 232, 0.8)",
            "rgba(138, 111, 249, 0.8)",
            "rgba(185, 168, 251, 0.8)",
            "rgba(233, 236, 239, 0.8)",
          ],
          hoverOffset: 20,
          borderWidth: 0,
        },
      ],
    },
    options: {
      cutout: "60%",
      plugins: {
        legend: {
          labels: {
            color: document.body.classList.contains("light-mode")
              ? "#000"
              : "#fff",
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.raw || 0;
              const total = context.chart.getDatasetMeta(0).total;
              const percentage =
                total > 0 ? ((value / total) * 100).toFixed(1) + "%" : "0%";
              return `${label}: ${value} (${percentage})`;
            },
          },
        },
      },
    },
  });

  const datePicker = document.getElementById("date-picker");
  if (datePicker) {
    datePicker.addEventListener("change", function () {
      document.getElementById("datePickerForm").submit();
    });
  }
});
