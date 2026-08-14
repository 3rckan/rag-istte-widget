# QA automatizado — burbuja flotante

Pruebas de interfaz con [Playwright](https://playwright.dev/python/) sobre
`app/static/widget.html` y `app/static/widget-loader.js`. Verifican que la
burbuja aparezca, que el panel abra/cierre, que se muestren mensajes y
fuentes, y el manejo de error de red. El endpoint `/query` se **mockea**
(`page.route`) para que las pruebas sean rápidas y no dependan de que
Ollama esté corriendo — la calidad de las respuestas del modelo la evalúa
`scripts/evaluate.py` por separado (Sprint 4), no esta suite.

## Instalación (una sola vez)

```
pip install -r requirements-qa.txt
playwright install chromium
```

## Cómo correrlas

1. Levantar el backend en otra terminal:
   ```
   uvicorn app.main:app --reload
   ```
2. Correr la suite:
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
