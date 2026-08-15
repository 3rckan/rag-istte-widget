# Dockerfile - Sprint 4 (despliegue en Render.com)
#
# Empaqueta la API (FastAPI) y Ollama (con los modelos ya descargados) en
# una sola imagen, porque Render solo expone un puerto por servicio web y
# el plan gratuito no permite levantar dos servicios conectados entre si
# sin pagar. Ver docs/DEPLOY_RENDER.md para los requisitos de RAM.

FROM python:3.11-slim

# 1. Instalar Ollama (se deja curl instalado: lo usa entrypoint.sh para
#    esperar a que el servidor de Ollama este listo antes de arrancar la API)
#
# NOTA DE SEGURIDAD (riesgo aceptado, ver docs/DEPLOY_RENDER.md): esto baja y
# ejecuta un script de instalacion remoto sin verificar checksum. Es un patron
# comun en la industria para instaladores de un solo comando, pero implica
# confiar en que ollama.com y la cadena HTTPS no esten comprometidos en el
# momento del build. No se aplico una alternativa con verificacion de hash
# porque Ollama no publica un checksum estable por version para ese script.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://ollama.com/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Descargar los modelos durante el build para que queden dentro de la
#    imagen (evita re-descargar ~2.3 GB cada vez que arranca el contenedor)
RUN ollama serve & \
    sleep 5 && \
    ollama pull llama3.2 && \
    ollama pull nomic-embed-text && \
    pkill ollama

# 4. Copiar el resto del proyecto
COPY app/ app/
COPY src/ src/
COPY scripts/ scripts/
COPY data/ data/

# 5. Ingesta inicial: genera chroma_db/ dentro de la imagen a partir de lo
#    que haya en data/reglamentos/ en el momento del build. Si se agregan
#    o cambian PDFs, hay que reconstruir y volver a desplegar la imagen.
RUN ollama serve & \
    sleep 5 && \
    python scripts/ingest.py && \
    pkill ollama

ENV OLLAMA_BASE_URL=http://localhost:11434
ENV PORT=8000

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 6. Usuario no-root (hallazgo de seguridad: antes todo corria como root).
#    Los modelos se descargaron en el paso 3 al $HOME de root (/root/.ollama);
#    se copian al $HOME del usuario nuevo para que Ollama los siga
#    encontrando una vez que dejamos de correr como root.
RUN useradd -m appuser \
    && mkdir -p /home/appuser/.ollama \
    && cp -r /root/.ollama/. /home/appuser/.ollama/ \
    && chown -R appuser:appuser /home/appuser /app
USER appuser

EXPOSE 8000
CMD ["./entrypoint.sh"]
