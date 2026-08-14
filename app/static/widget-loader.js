/**
 * widget-loader.js — burbuja flotante del Asistente Virtual ISTTE.
 *
 * Uso: pegar en cualquier pagina (sitio publico ISTTE o EVA/Moodle)
 *   <script src="https://TU-DOMINIO/widget/widget-loader.js"></script>
 *
 * No requiere configuracion: calcula solo la URL del backend a partir
 * de donde esta alojado este mismo script (document.currentScript),
 * asi que sirve igual en local (http://127.0.0.1:8000) que en produccion.
 */
(function () {
  "use strict";

  var scriptEl = document.currentScript;
  var origen = new URL(scriptEl.src).origin;
  var srcIframe = origen + "/widget/widget.html";

  var ANCHO = 380;
  var ALTO = 560;
  var MARGEN = 20;

  var estilos = document.createElement("style");
  estilos.textContent = [
    "#istte-chat-burbuja {",
    "  position: fixed; right: " + MARGEN + "px; bottom: " + MARGEN + "px;",
    "  width: 60px; height: 60px; border-radius: 50%;",
    "  background: linear-gradient(135deg, #1a3c6e, #12294d);",
    "  box-shadow: 0 4px 14px rgba(0,0,0,0.25);",
    "  border: none; cursor: pointer; z-index: 2147483000;",
    "  display: flex; align-items: center; justify-content: center;",
    "  transition: transform 0.15s ease;",
    "}",
    "#istte-chat-burbuja:hover { transform: scale(1.06); }",
    "#istte-chat-burbuja svg { width: 28px; height: 28px; }",
    "#istte-chat-panel {",
    "  position: fixed; right: " + MARGEN + "px;",
    "  bottom: " + (MARGEN + 60 + 12) + "px;",
    "  width: " + ANCHO + "px; height: " + ALTO + "px;",
    "  max-width: calc(100vw - " + (MARGEN * 2) + "px);",
    "  max-height: calc(100vh - " + (MARGEN * 2 + 60 + 12) + "px);",
    "  border-radius: 14px; overflow: hidden;",
    "  box-shadow: 0 8px 30px rgba(0,0,0,0.28);",
    "  z-index: 2147483000;",
    "  opacity: 0; transform: translateY(12px); pointer-events: none;",
    "  transition: opacity 0.18s ease, transform 0.18s ease;",
    "}",
    "#istte-chat-panel.abierto { opacity: 1; transform: translateY(0); pointer-events: auto; }",
    "#istte-chat-panel iframe { width: 100%; height: 100%; border: none; display: block; }",
    "@media (max-width: 480px) {",
    "  #istte-chat-panel {",
    "    right: 10px; left: 10px; width: auto;",
    "    bottom: " + (MARGEN + 60 + 8) + "px;",
    "  }",
    "}"
  ].join("\n");
  document.head.appendChild(estilos);

  var burbuja = document.createElement("button");
  burbuja.id = "istte-chat-burbuja";
  burbuja.type = "button";
  burbuja.setAttribute("aria-label", "Abrir asistente virtual ISTTE");
  burbuja.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>' +
    "</svg>";

  var panel = document.createElement("div");
  panel.id = "istte-chat-panel";
  var iframe = document.createElement("iframe");
  iframe.src = srcIframe;
  iframe.title = "Asistente Virtual ISTTE";
  panel.appendChild(iframe);

  var abierto = false;
  function alternar(forzar) {
    abierto = typeof forzar === "boolean" ? forzar : !abierto;
    panel.classList.toggle("abierto", abierto);
    burbuja.setAttribute("aria-expanded", String(abierto));
  }

  burbuja.addEventListener("click", function () {
    alternar();
  });

  // El boton de cerrar dentro del iframe (widget.html) no puede tocar el
  // DOM del host por CORS, asi que avisa por postMessage.
  window.addEventListener("message", function (evento) {
    if (evento.origin === origen && evento.data && evento.data.tipo === "istte-chat-cerrar") {
      alternar(false);
    }
  });

  document.body.appendChild(panel);
  document.body.appendChild(burbuja);
})();
