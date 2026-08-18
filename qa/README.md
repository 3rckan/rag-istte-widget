# QA automatizado — burbuja flotante

Pruebas de interfaz con [Playwright](https://playwright.dev/python/) sobre
`app/static/widget.html` y `app/static/widget-loader.js`. Verifican que la
burbuja aparezca, que el panel abra/cierre, que se muestren mensajes y
fuentes, y el manejo de error de red. Tanto el endpoint `/query` como los
archivos estáticos del widget (`widget-loader.js`, `widget.html`) se
**mockean** (`page.route`), así que la suite es standalone: no depende de
que Ollama ni `uvicorn` estén corriendo — la calidad de las respuestas del
modelo la evalúa `scripts/evaluate.py` por separado (Sprint 4), y la
prueba manual contra el backend real se hace levantando `uvicorn` y
abriendo `qa/host_prueba.html` (ver `docs/EMBED_GUIDE.md`).

## Instalación (una sola vez)

```
pip install -r requirements-qa.txt
playwright install chromium
```

## Cómo correrlas

```
pytest qa/ -v
```

Para ver el navegador mientras corre (útil para depurar visualmente):

```
pytest qa/ --headed --slowmo 300
```

## Qué cubre cada prueba (`test_widget.py`)

- La burbuja se ve en la página host.
- El panel arranca cerrado.
- Click en la burbuja abre el panel con el iframe cargado.
- El botón de cerrar (dentro del iframe) cierra el panel vía `postMessage`.
- Enviar una pregunta muestra la respuesta y la fuente citada.
- Si el backend falla, se muestra el mensaje de error (no se rompe la UI).
- El panel es usable en viewports de celular (375px y 390px de ancho).
