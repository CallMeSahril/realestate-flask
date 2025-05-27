function setupDashboardView() {
  console.log("📊 Dashboard view loaded");

  const summaryBox = document.getElementById("summary-total-properties");
  if (summaryBox) {
    fetch("/api/properties/count")
      .then(res => res.json())
      .then(data => {
        summaryBox.textContent = `${data.total} properti`;
      })
      .catch(err => {
        console.error("❌ Gagal ambil data properti:", err);
        summaryBox.textContent = "Data tidak tersedia";
      });
  }
}

window.setupDashboardView = setupDashboardView;
