# Guía de embebido — burbuja flotante del Asistente Virtual ISTTE

Esta guía explica cómo insertar la burbuja de chat en una página existente
(el sitio público del instituto o el portal EVA/Moodle), y cómo probarla
en local antes de tocar el sitio real.

## Cómo funciona

- `app/static/widget.html` — el panel de chat en sí (header, mensajes,
  input). Está pensado para vivir dentro de un `<iframe>`, no para abrirse
  solo.
- `app/static/widget-loader.js` — el script que se pega en la página host.
  Crea el botón circular flotante (la "burbuja") y el `<iframe>` que carga
  `widget.html`, y maneja abrir/cerrar. No necesita configuración: calcula
  la URL del backend a partir de dónde está alojado él mismo.
- El botón de cerrar dentro del panel usa `postMessage` para avisarle al
  loader que oculte el panel (un iframe no puede tocar el DOM de la
  página que lo embebe directamente).

## Probarlo en local (antes de tocar el sitio real)

1. Levantar el backend:
   ```
   uvicorn app.main:app --reload
   ```
2. Abrir `qa/host_prueba.html` directamente en el navegador (doble clic,
   o `file:///.../qa/host_prueba.html`). Esa página simula un host con
   fondo claro (como EVA) e incluye el loader apuntando a
   `http://127.0.0.1:8000`.
3. Debería aparecer la burbuja azul abajo a la derecha. Click para abrir
   el panel y probar una pregunta real contra el RAG.

Esto es exactamente el mismo mecanismo que se usará en el sitio real —
solo cambia la URL del `<script src="...">`.

## Embeber en el sitio público (istte.edu.ec)

Agregar antes de `</body>`, en la plantilla del sitio (o en el bloque de
"HTML personalizado" si el sitio usa un CMS):

```html
<script src="https://TU-DOMINIO-DE-RENDER/widget/widget-loader.js"></script>
```

**Nota de diseño:** el sitio público ya tiene una burbuja de WhatsApp
abajo a la izquierda. La burbuja del asistente se ubicó abajo a la
**derecha** a propósito para no superponerse.

## Embeber en EVA (Moodle)

Moodle permite inyectar HTML/JS sin tocar el tema, desde
**Administración del sitio → Apariencia → HTML adicional**, campo
"Antes de `</body>`":

```html
<script src="https://TU-DOMINIO-DE-RENDER/widget/widget-loader.js"></script>
```

Esto requiere permisos de administrador del sitio Moodle (no de un curso
individual) — hay que coordinarlo con quien administra la instancia EVA
del instituto. Si no se tiene ese acceso todavía, la prueba en
`qa/host_prueba.html` sirve como validación funcional mientras se gestiona
el acceso.

## CORS en producción

Por defecto (`app/main.py`) el backend acepta peticiones desde cualquier
origen (`*`), útil para probar. Antes de desplegar, fijar
`ALLOWED_ORIGINS` en el `.env` (o en las variables de entorno de Render)
con los dominios reales, separados por coma:

```
ALLOWED_ORIGINS=https://istte.edu.ec,https://eva.tecnovirtual.edu.ec
```

Ver también `docs/DEPLOY_RENDER.md` para el resto de la configuración de
despliegue.
