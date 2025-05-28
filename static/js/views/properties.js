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

  // Load provinsi dari backend Flask
  fetch("/api/provinces")
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        console.error("❌ Gagal ambil provinsi:", data.error);
        alert("❌ Gagal ambil data provinsi: " + data.error);
        return;
      }

      const selectProvinsi = document.getElementById("provinsi");
      data.forEach(prov => {
        const opt = document.createElement("option");
        opt.value = prov.name;
        opt.textContent = prov.name;
        opt.dataset.id = prov.id;
        selectProvinsi.appendChild(opt);
      });
    })
    .catch(err => {
      console.error("❌ Error fetch provinces:", err);
      alert("Gagal terhubung ke server.");
    });


  // Load kota dari backend Flask ketika provinsi dipilih
  const selectProvinsi = document.getElementById("provinsi");
  if (selectProvinsi) {
    selectProvinsi.addEventListener("change", function () {
      const provId = this.selectedOptions[0].dataset.id;
      const kotaSelect = document.getElementById("kota");
      if (!kotaSelect) return;

      kotaSelect.innerHTML = `<option value="">Memuat...</option>`;

      fetch(`/api/cities/${provId}`)
        .then(res => res.json())
        .then(data => {
          kotaSelect.innerHTML = `<option value="">Pilih Kota/Kabupaten</option>`;
          data.forEach(city => {
            const opt = document.createElement("option");
            opt.value = city.name;
            opt.textContent = city.name;
            kotaSelect.appendChild(opt);
          });
        });
    });
  }
}

// Daftarkan ke global agar bisa dipanggil dari controller.js
window.setupPropertiesView = setupPropertiesView;
