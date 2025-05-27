document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("view-container");

  function loadView(view) {
    fetch(`/view/${view}`)  // ✅ Ganti jadi "/view/" sesuai Flask route
      .then(res => res.text())
      .then(html => {
        container.innerHTML = html;
      });
  }
  document.querySelector('[data-view="recommendations"]').addEventListener("click", async () => {
    const view = "recommendations";
    const res = await fetch(`/view/${view}`);
    const html = await res.text();
    document.getElementById('view-container').innerHTML = html;

    // Tambahkan script sesuai view
    const script = document.createElement("script");
    script.src = `/static/js/views/${view}.js`; // ✅ backtick di sini
    script.onload = () => {
      const fn = window[`setup${view.charAt(0).toUpperCase() + view.slice(1)}View`];
      if (typeof fn === "function") {
        fn();
      } else {
        console.error("❌ Function tidak ditemukan untuk:", view);
      }
    };
    document.body.appendChild(script);
  });


  document.querySelectorAll("[data-view]").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const view = e.target.getAttribute("data-view");
      loadView(view);
    });
  });

  // Load default view saat pertama kali
  loadView("dashboard");
});
