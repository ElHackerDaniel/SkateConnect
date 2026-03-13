// scripts.js - ReservaSkate (animaciones extra: loaders, stagger, chart helpers)
document.addEventListener('DOMContentLoaded', function() {
  // --- Auto-dismiss flash messages (existente) ---
  const wrapper = document.getElementById('flash-wrapper');
  if (wrapper) {
    wrapper.querySelectorAll('.flash').forEach((el, idx) => {
      const close = el.querySelector('.flash-close');
      if (close) close.addEventListener('click', () => el.remove());
      // staggered auto dismiss
      setTimeout(() => { if (el.parentNode) el.remove(); }, 4500 + idx * 300);
    });
  }

  // --- Confirm helper (existente) ---
  document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', function(e) {
      const msg = form.getAttribute('data-confirm') || '¿Confirmar?';
      if (!confirm(msg)) e.preventDefault();
    });
  });

  // --- Staggered reveal for .card elements on page load ---
  const cards = document.querySelectorAll('.card');
  cards.forEach((c, i) => {
    c.style.opacity = 0;
    c.style.transform = 'translateY(10px)';
    setTimeout(() => {
      c.style.transition = 'transform 450ms cubic-bezier(.2,.9,.2,1), opacity 450ms ease';
      c.style.opacity = 1;
      c.style.transform = 'translateY(0)';
    }, 120 + i * 80);
  });

  // --- Chart loader helpers ---
  window.showChartLoader = function(chartContainerId) {
    const cont = document.getElementById(chartContainerId);
    if (!cont) return;
    // create loader overlay if not exists
    if (!cont.querySelector('.chart-loader')) {
      const loader = document.createElement('div');
      loader.className = 'chart-loader';
      loader.innerHTML = `<div class="dotdot"><div></div><div></div><div></div></div>`;
      loader.style.position = 'absolute';
      loader.style.inset = '0';
      loader.style.display = 'flex';
      loader.style.alignItems = 'center';
      loader.style.justifyContent = 'center';
      loader.style.background = 'linear-gradient(180deg, rgba(11,16,20,0.6), rgba(11,16,20,0.6))';
      loader.style.borderRadius = '10px';
      cont.style.position = 'relative';
      cont.appendChild(loader);
    }
  };

window.hideChartLoader = function(chartContainerId) {
  const cont = document.getElementById(chartContainerId);
  if (!cont) return;

  const loader = cont.querySelector('.chart-loader');
  if (loader) {
    loader.classList.add("removed");   // <-- fuerza desaparición
    loader.remove();                   // <-- desaparece del DOM
  }
};

  // --- Nice Chart.js init wrapper: animates datasets entry ---
  window.createAnimatedChart = function (canvas, cfg) {

    // -----------------------------
    // Ajustes globales por defecto
    // -----------------------------
    cfg.options = cfg.options || {};
    cfg.options.maintainAspectRatio = false;
    cfg.options.responsive = true;

    cfg.options.animation = cfg.options.animation || {};
    cfg.options.animation.duration = cfg.options.animation.duration || 900;
    cfg.options.animation.easing = cfg.options.animation.easing || "easeOutQuart";

    cfg.options.elements = cfg.options.elements || {};
    cfg.options.elements.point = cfg.options.elements.point || { radius: 4 };

    cfg.options.plugins = cfg.options.plugins || {};
    cfg.options.plugins.legend = cfg.options.plugins.legend || { display: false };

    // ---------------------------------------------------------
    // FIX: Mejora automática de visibilidad en gráficos de fechas
    // Se aplica SOLO si el gráfico es lineal y tiene etiquetas largas.
    // ---------------------------------------------------------
    if (cfg.type === "line" && cfg.data && Array.isArray(cfg.data.labels)) {
        cfg.options.scales = cfg.options.scales || {};

        cfg.options.scales.x = cfg.options.scales.x || {
            ticks: {
                maxRotation: 0,
                minRotation: 0,
                callback: function (value, index, ticks) {
                    const raw = ticks[index].label;
                    if (!raw) return "";
                    
                    // Si viene algo como "2025-01-11 00:00:00 GMT"
                    // → devolvemos solo "2025-01-11"
                    return raw.split(" ")[0];
                }
            }
        };

        cfg.options.scales.y = cfg.options.scales.y || {
            beginAtZero: true
        };
    }

    // ------------------------------------------------------------------
    // ANIMACIÓN: todos los datasets empiezan en 0 y luego suben animados
    // ------------------------------------------------------------------
    if (cfg.data && cfg.data.datasets) {
        cfg.data.datasets.forEach(ds => {
            ds._realData = ds.data.slice();
            ds.data = ds.data.map(() => 0);
        });
    }

    const chart = new Chart(canvas, cfg);

    setTimeout(() => {
        if (cfg.data && cfg.data.datasets) {
            cfg.data.datasets.forEach(ds => {
                ds.data = ds._realData.slice();
            });
            chart.update();
        }
    }, 120);

    return chart;
};
});

