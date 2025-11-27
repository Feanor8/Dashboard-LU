document.addEventListener('DOMContentLoaded', function () {
  if (typeof Plotly === 'undefined') {
    console.error('Plotly nicht geladen.');
    return;
  }
  const graphs = window.PLOT_DATA || {};
  if (!Object.keys(graphs).length) {
    console.warn('Keine Graphdaten in window.PLOT_DATA.');
    return;
  }

  Object.entries(graphs).forEach(([domId, figure]) => {
    let el = document.getElementById(domId);
    if (!el) {
      console.warn(`Kein Element mit id="${domId}" gefunden. Chart wird nicht gerendert.`);
      return; // skip rendering
    }

    // responsive sizing, may be fucky
    // el.style.height = el.dataset.height || '350px';

    try {
      if (figure.data) {
        // Plotly.react für effizientes Updates statt newPlot, wenn später dynamisch aktualisiere
        // aber ist eigentlich unwichtig für unseren ANwendungsfall
        Plotly.react(el, figure.data, figure.layout || {});
      } else {
        Plotly.react(el, figure);
      }
    } catch (err) {
      console.error(`Fehler beim Rendern von ${domId}:`, err);
      el.innerText = 'Fehler beim Rendern des Charts.';
    }
  });

  // ⬇️ ADD YOUR FETCH CODE HERE
  fetch("data/Stadtteil.html")
    .then(response => response.text())
    .then(html => {
      document.getElementById("karte-container").innerHTML = html;
    })
    .catch(error => {
      console.error("Fehler beim Laden der Datei:", error);
    });

});