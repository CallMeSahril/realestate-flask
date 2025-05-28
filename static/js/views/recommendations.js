function setupRecommendationsView() {
  console.log("✨ Recommendations view loaded");

  const form = document.getElementById("recommendation-form");
  const selectLocation = document.getElementById("preferred_location");
  const resultsContainer = document.getElementById("recommendation-results");

  if (!form || !selectLocation || !resultsContainer) {
    console.warn("⚠️ Form atau elemen penting tidak ditemukan di halaman.");
    return;
  }

  async function loadLocations() {
    try {
      const res = await fetch("locations");
      const locations = await res.json();
      selectLocation.innerHTML = '<option value="">Pilih lokasi...</option>';
      locations.forEach(loc => {
        const option = document.createElement("option");
        option.value = loc;
        option.textContent = loc;
        selectLocation.appendChild(option);
      });
    } catch (err) {
      console.error("❌ Gagal memuat lokasi:", err);
    }
  }

  function getWeightsByCategory(category) {
    const base = { location: 1, type: 1, price: 1, size: 1, rooms: 1 };
    switch (category) {
      case "location": base.location = 2; break;
      case "type":     base.type = 2; break;
      case "price":    base.price = 2; break;
      case "size":     base.size = 2; break;
      case "rooms":    base.rooms = 2; break;
    }
    return base;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      preferred_location: selectLocation.value,
      preferred_type: document.getElementById("preferred_type").value,
      budget: parseFloat(document.getElementById("budget").value),
      building_size: parseFloat(document.getElementById("building_size").value),
      num_rooms: parseInt(document.getElementById("num_rooms").value),
      weights: getWeightsByCategory(document.getElementById("priority_category").value)
    };

    try {
      const res = await fetch("/recommendations/by-profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      resultsContainer.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        resultsContainer.innerHTML = "<p class='text-red-600'>Tidak ada hasil yang cocok.</p>";
        return;
      }

      data.forEach(prop => {
        resultsContainer.innerHTML += `
          <div class="bg-white p-4 rounded shadow border">
            <h3 class="text-lg font-bold">${prop.title}</h3>
            <p class="text-sm text-gray-600">${prop.location} • ${prop.type}</p>
            <p class="text-sm">Harga: Rp${prop.price.toLocaleString()}</p>
            <p class="text-sm">Ukuran: ${prop.building_size} m² • Kamar: ${prop.num_rooms}</p>
            <p class="text-green-600 text-sm mt-2">Skor Kecocokan: ${(prop.score * 100).toFixed(1)}%</p>
          </div>
        `;
      });

    } catch (err) {
      console.error("❌ Gagal mengambil rekomendasi:", err);
      resultsContainer.innerHTML = "<p class='text-red-600'>Terjadi kesalahan saat mengambil data.</p>";
    }
  });

  // Panggil saat view di-load
  loadLocations();
}

// Register ke global
window.setupRecommendationsView = setupRecommendationsView;
