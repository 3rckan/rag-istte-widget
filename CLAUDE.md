# Contexto del proyecto — leer antes de ayudar

Este es el proyecto de titulación de Erick Andrés Guachamin Torres (P41 Modular, Desarrollo de Software) en el Instituto Superior Tecnológico Tecnoecuatoriano (ISTTE): un asistente virtual basado en RAG (Retrieval-Augmented Generation) para direccionamiento estudiantil.

## Arquitectura fija (no cambiar sin avisar)

- Servicio desacoplado: backend API (FastAPI) independiente + widget de chat embebible en la web del instituto.
- **Ollama** sirviendo **Llama 3.2** como modelo generativo local.
- **nomic-embed-text** (vía Ollama) para los embeddings.
- **ChromaDB** como vector store, persistido en disco (`chroma_db/`).
- **LangChain** para orquestar el pipeline RAG (chunking, retrieval, prompting).
- Python 3.11, entorno virtual en `venv/`.

## Plan del proyecto (Scrum, 5 sprints, 26 may – 27 jul 2026)

- **Sprint 1 (26 may – 08 jun):** entorno de desarrollo + recopilación de PDFs oficiales del instituto. **Estado: casi listo** — venv creado, Ollama instalado, faltan `pip install -r requirements.txt` y descargar los modelos (`ollama pull llama3.2`, `ollama pull nomic-embed-text`). Los PDFs de reglamentos/calendarios todavía no están recopilados (pendiente de secretaría).
- **Sprint 2 (09 jun – 22 jun):** pipeline de ingesta + base vectorial ChromaDB. `scripts/ingest.py` existe como esqueleto con TODOs, sin implementar todavía.
- **Sprint 3 (23 jun – 06 jul):** endpoint `/query` en FastAPI + widget de chat HTML/JS embebible + CORS.
- **Sprint 4 (07 jul – 20 jul):** evaluación con 30 consultas reales + despliegue en Render.com.
- **Sprint 5 (21 jul – 27 jul):** memoria técnica y defensa oral.

## Cómo ayudar a Andrés (importante)

Andrés está evaluado en que **él entienda y escriba el código**, no solo en que el proyecto funcione. Su nivel es junior-bajo: piensa bien lógicamente pero todavía no tiene soltura en Python, está reforzando fundamentos en paralelo.

- Explica el concepto antes de tocar código, con una analogía corta.
- Da estructura (funciones con nombres y `# TODO`), no el archivo completo resuelto.
- Si revisas código suyo con errores: señala qué falla y por qué, no lo reescribas tú.
- En depuración: haz 1-2 preguntas para que él lea el error primero, antes de dar la solución directa.
- Excepciones donde SÍ puedes dar código completo sin rodeos: si él lo pide explícitamente, si hay presión real de entrega, o si es configuración/boilerplate no pedagógico (instalar dependencias, estructura de carpetas, comandos de terminal).
- Si el cambio de código tiene implicación para la tesis (decisión de arquitectura, limitación técnica, resultado de evaluación), dilo explícitamente — le sirve para escribir el Capítulo 2 o 4 del documento.

## Estructura del repo

```
rag-istte-widget/
├── data/reglamentos/   # PDFs oficiales del instituto (aún vacío)
├── scripts/ingest.py   # Script de ingesta — esqueleto sin implementar (Sprint 2)
├── src/                # Lógica del backend RAG (Sprint 2-3, aún vacío)
├── app/                # Endpoints FastAPI (Sprint 3, aún vacío)
├── requirements.txt
└── README.md           # Checklist de estado del Sprint 1
```
