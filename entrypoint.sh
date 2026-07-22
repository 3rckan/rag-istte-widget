#!/bin/sh
# entrypoint.sh - arranca Ollama en segundo plano y luego la API.
# chroma_db/ ya viene generado desde el build del Dockerfile.
set -e

ollama serve &

echo "Esperando a que Ollama este listo..."
until curl -sf http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done
echo "Ollama listo."

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
