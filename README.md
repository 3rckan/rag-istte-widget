# Asistente Virtual RAG — ISTTE

Plug-in de asistencia virtual basado en IA Generativa (Llama 3.2 + Ollama) y arquitectura RAG (ChromaDB + LangChain) para el direccionamiento estudiantil del Instituto Superior Tecnológico Tecnoecuatoriano.

Servicio desacoplado: backend API (FastAPI) independiente + widget de chat embebible en la plataforma web del instituto.

## Estado: Sprint 1 — Requerimientos y entorno (26 may – 08 jun 2026)

- [x] Estructura de carpetas del proyecto
- [x] `requirements.txt` con dependencias base
- [x] `.gitignore` configurado
- [x] Repositorio Git inicializado con primer commit
- [ ] Entorno virtual Python 3.11 creado e instalado (`python -m venv venv` — en tu máquina)
- [x] Ollama instalado
- [ ] Modelos descargados en Ollama (`llama3.2` y `nomic-embed-text`) — ver comandos abajo
- [ ] PDFs de reglamentos, calendarios y guías del instituto recopilados en `data/reglamentos/` (**no se encontraron PDFs de reglamentos en tu Drive — ver sección abajo**)

## Estructura del proyecto

```
rag-istte-widget/
├── data/
│   └── reglamentos/       # Aquí van los PDFs oficiales del instituto (US-01)
├── scripts/
│   └── ingest.py          # Script de ingesta (Sprint 2, aún no implementado)
├── src/
│   └── (lógica del backend RAG — Sprint 2-3)
├── app/
│   └── (endpoints FastAPI — Sprint 3)
├── requirements.txt
├── .gitignore
└── README.md
```

## Pendiente de recopilar (US-01)

Al revisar tu Google Drive no se encontraron PDFs de reglamentos, mallas o calendarios del ISTTE — solo material de inglés (IELTS). Para cerrar esta tarea necesitas conseguir y subir a `data/reglamentos/`:

1. Reglamento de Régimen Académico del instituto.
2. Calendario académico / de matrículas vigente.
3. Guías de trámites administrativos (secretaría, validación de conocimientos, etc.).

Estos documentos normalmente los entrega secretaría o coordinación — tu nota en Miro ("pedir lunes 01/06 documentos en secretaría") sugiere que esa gestión ya estaba planeada.

## Siguiente paso manual (en tu computadora, no en este entorno)

Ollama ya está instalado. Falta:

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Descargar los dos modelos que usa el proyecto:
#    - llama3.2: el modelo generativo (responde al estudiante)
#    - nomic-embed-text: el modelo de embeddings (convierte texto en vectores para ChromaDB)
ollama pull llama3.