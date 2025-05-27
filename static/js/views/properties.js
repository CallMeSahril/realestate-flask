function setupPropertiesView() {
  console.log("🏘️ Properties view loaded");

  // Tombol hapus properti
  document.querySelectorAll("[data-delete-id]").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-delete-id");
      if (!confirm("Yakin ingin menghapus properti ini?")) return;

      try {
        const res = await fetch(`/delete-property/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (data.status === "deleted") {
          alert("✅ Properti berhasil dihapus.");
          location.reload();
        } else {
          alert("❌ Gagal menghapus properti.");
        }
      } catch (err) {
        console.error("❌ Error saat menghapus:", err);
        alert("❌ Terjadi kesalahan.");
      }
    });
  });

  // Tombol print
  const printBtn = document.getElementById("btn-print-table");
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }
}

// Daftarkan ke global agar dipanggil controller.js
window.setupPropertiesView = setupPropertiesView;
