// static/js/views/dashboard.js
(async () => {
  console.log("✅ SCRIPT DIJALANKAN");

  try {
    const res = await fetch("/api/dashboard-summary");
    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
    const data = await res.json();
    console.log("✅ Data dashboard:", data);

    document.getElementById("summary-total-properties").innerText = data.total_properties ?? 0;
    document.getElementById("summary-consultation").innerText = data.consultations_today ?? 0;
    document.getElementById("summary-follow-up").innerText = data.follow_ups_pending ?? 0;

    const activityList = document.getElementById("activity-list");
    activityList.innerHTML = "";
    data.latest_activities.forEach(item => {
      const li = document.createElement("li");
      li.className = "py-2 flex items-center justify-between";
      li.innerHTML = `<span>${item.desc}</span><span class="text-xs text-gray-400">${item.time}</span>`;
      activityList.appendChild(li);
    });

    const map = L.map('property-map').setView([-6.2, 106.8], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    data.properties_location.forEach(p => {
      if (p.lat && p.lng) {
        const marker = L.marker([p.lat, p.lng]).addTo(map);
        marker.bindPopup(`<strong>${p.title}</strong><br><button class="text-blue-600 underline detail-btn" data-id="${p.id}">Lihat Detail</button>`);

        marker.on('click', () => {
          console.log("📍 Marker diklik:", p.title);
          showPropertyDetail(p);
        });
      }
    });

  } catch (err) {
    console.error("❌ Gagal memuat data dashboard:", err);
    alert("Gagal memuat data dashboard.");
  }
})();

// Tetap di luar async: fungsi utilitas
function showPropertyDetail(p) {
  const detailDiv = document.getElementById("property-detail");
  const content = `
    <p><strong>Judul:</strong> ${p.title}</p>
    <p><strong>Lokasi:</strong> ${p.location}</p>
    <p><strong>Tipe:</strong> ${p.type || '-'}</p>
    <p><strong>Harga:</strong> Rp ${Number(p.price).toLocaleString()}</p>
    <p><strong>Luas Bangunan:</strong> ${p.building_size} m²</p>
    <p><strong>Kamar:</strong> ${p.num_rooms}</p>
    <p><strong>Fitur:</strong> ${p.fitur || '-'}</p>
    ${p.gambar ? `<img src="${p.gambar}" class="mt-2 rounded shadow w-full max-w-sm">` : ''}
  `;
  document.getElementById("detail-content").innerHTML = content;
  detailDiv.classList.remove("hidden");
}
