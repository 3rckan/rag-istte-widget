# Despliegue en Render.com — Sprint 4

## ⚠️ Limitación técnica importante (para el capítulo de resultados/limitaciones de la tesis)

La arquitectura del proyecto usa **Ollama local** sirviendo **Llama 3.2** (~2 GB) y
**nomic-embed-text** para los embeddings. Estos modelos corren en CPU y necesitan
varios GB de RAM disponibles para responder sin timeouts.

Los planes económicos de Render (**Free** y **Starter**, 512 MB de RAM) **no
alcanzan** para correr Ollama con estos modelos — el contenedor se queda sin
memoria al cargar `llama3.2`. Esto obliga a usar como mínimo el plan
**Standard** (2 GB RAM, de pago) o superior.

**Esto es una limitación real de la arquitectura elegida** (Ollama local vs. un
LLM por API en la nube), no un bug. Vale la pena documentarla explícitamente
en la memoria técnica: es el tipo de trade-off que se espera que un proyecto
de titulación identifique y justifique (costo/control de datos en el instituto
vs. dependencia de un proveedor externo de LLM).

Si el instituto no puede costear un plan de pago, la alternativa sin cambiar
de arquitectura es desplegar el contenedor en una VM propia del instituto (o
un servicio con más RAM gratis, si existe) en vez de Render.

## Qué se preparó

- **`Dockerfile`**: empaqueta la API + Ollama + los modelos (descargados
  durante el build) + la base ChromaDB ya generada a partir de lo que haya
  en `data/reglamentos/` en ese momento.
- **`entrypoint.sh`**: arranca Ollama, espera a que esté listo y recién ahí
  levanta `uvicorn`.
- **`render.yaml`**: define el servicio web tipo Docker, con las variables
  de entorno `ALLOWED_ORIGINS` y `OLLAMA_BASE_URL`.
- **`.env.example`**: referencia de las variables de entorno usadas en
  desarrollo local.

## Pasos para desplegar (manual, requiere tu cuenta de Render)

1. Reemplazá los PDFs de ejemplo en `data/reglamentos/` por los oficiales
   del ISTTE (ver pendiente del Sprint 1) y corré `python scripts/ingest.py`
   localmente para confirmar que el resultado es el esperado.
2. Commiteá y subí el repo a GitHub (necesario porque Render se conecta a un
   repositorio Git).
3. En [render.com](https://render.com), creá un **New Web Service** →
   **Build and deploy from a Git repository** → elegí el repo.
4. Render debería detectar el `render.yaml` automáticamente (Blueprint). Si
   no, configurá manualmente:
   - **Runtime**: Docker
   - **Plan**: Standard (2 GB) o superior — ver limitación arriba
   - **Environment Variables**: `ALLOWED_ORIGINS` = dominio real de la web
     del instituto
5. Desplegar. El primer build tarda varios minutos (descarga los modelos de
   Ollama dentro de la imagen).
6. Una vez arriba, el widget queda accesible en
   `https://<tu-servicio>.onrender.com/widget/` y se puede embeber con un
   `<iframe>` en la web del instituto. El endpoint `/query` no necesita
   configurarse aparte porque el widget usa una URL relativa.

## Cómo actualizar los PDFs ya desplegado

Como la ingesta corre durante el *build* de la imagen (no en cada arranque),
para actualizar los documentos hay que:
1. Reemplazar los PDFs en `data/reglamentos/`.
2. Commitear y hacer push.
3. Redesplegar en Render (o dejar que el auto-deploy lo haga si está
   habilitado) — esto vuelve a correr `ingest.py` dentro del build.
