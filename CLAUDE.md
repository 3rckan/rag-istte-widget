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

- **Sprint 1 (26 may – 08 jun):** entorno de desarrollo + recopilación de PDFs oficiales del instituto. **Estado: entorno listo** (venv, Ollama, modelos descargados). **Bloqueado:** los PDFs oficiales de reglamentos/calendarios del ISTTE siguen sin llegar de secretaría — el proyecto sigue trabajando con 2 PDFs de ejemplo/ficticios en `data/reglamentos/`. Esto es un bloqueo externo, no técnico.
- **Sprint 2 (09 jun – 22 jun):** pipeline de ingesta + base vectorial ChromaDB. **Estado: implementado y probado** (`scripts/ingest.py`) contra los PDFs de ejemplo. Pendiente reingestar cuando lleguen los oficiales.
- **Sprint 3 (23 jun – 06 jul):** endpoint `/query` en FastAPI + widget de chat HTML/JS embebible + CORS. **Estado: completo**, probado de punta a punta, commiteado.
- **Sprint 4 (07 jul – 20 jul):** evaluación con 30 consultas + despliegue en Render.com. **Estado: infraestructura lista** — `scripts/evaluate.py` corrido (30/30 sin errores, ver `docs/evaluacion/`) y config de despliegue (`Dockerfile`, `render.yaml`, `docs/DEPLOY_RENDER.md`) preparada. **Pendiente:** la evaluación es solo sobre datos de ejemplo (hay que repetirla con los PDFs oficiales) y el despliegue real en Render requiere que Andrés cree la cuenta y elija un plan de pago (ver limitación de RAM documentada en `docs/DEPLOY_RENDER.md`) — no se puede hacer desde este entorno.
- **Sprint 5 (21 jul – 27 jul):** memoria técnica y defensa oral. **Estado: en progreso** — estructura y contenido de arquitectura/decisiones ya redactados en `docs/memoria/`; los capítulos de resultados y conclusiones dependen de la evaluación con datos reales y del trabajo personal de Andrés (ver nota pedagógica abajo).

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
├── data/reglamentos/       # Solo PDFs de ejemplo — los oficiales del instituto siguen pendientes
├── scripts/ingest.py       # Pipeline de ingesta (Sprint 2, implementado)
├── scripts/evaluate.py     # Evaluación con 30 consultas (Sprint 4)
├── src/rag_chain.py        # Lógica del backend RAG (Sprint 2-3)
├── app/main.py              # Endpoint /query + monta /widget (Sprint 3)
├── app/static/widget.html   # Panel de chat (vive dentro de un iframe)
├── app/static/widget-loader.js # Burbuja flotante embebible en cualquier página host
├── qa/                       # QA automatizado (Playwright) de la burbuja — ver qa/README.md
├── docs/EMBED_GUIDE.md      # Cómo embeber la burbuja en istte.edu.ec y EVA/Moodle
├── docs/evaluacion/        # Reportes de evaluación (Sprint 4)
├── docs/memoria/           # Borrador de memoria técnica (Sprint 5)
├── Dockerfile, render.yaml # Config de despliegue (Sprint 4)
├── requirements.txt
├── requirements-qa.txt      # Dependencias solo para QA (playwright, pytest)
└── README.md                # Checklist de estado por sprint
```

## gstack (skills de Claude Code instalados)

Se instaló [gstack](https://github.com/garrytan/gstack) como set de skills de Claude Code (`/qa`, `/review`, `/cso`, etc.), no como dependencia del proyecto.

**Regla:** la sección "Cómo ayudar a Andrés" arriba tiene prioridad sobre el comportamiento por defecto de cualquier skill de gstack. Concretamente:

- Usar `/qa-only` y `/review` en modo solo-reporte en vez de `/qa` (que auto-corrige bugs) — Andrés debe escribir sus propios fixes.
- `/cso` (auditoría de seguridad) y `/health` (dashboard de calidad) son de solo lectura, seguros de correr libremente.
- No usar `/ship` ni `/land-and-deploy` sin confirmación explícita — hacen push/merge/deploy real.
- `/document-generate` no debe usarse para redactar los capítulos de la memoria técnica (Sprint 5) — esos son trabajo personal de Andrés.

## Diseño de la burbuja flotante (rediseño post-Sprint 3)

El widget se rediseñó como burbuja flotante embebible (antes era un panel
de chat estático centrado en la página). Referencia visual tomada de
capturas reales de `istte.edu.ec` (azul `#1a3c6e` / verde `#6fae2e`
institucionales) y del portal EVA (Moodle, tema claro y minimalista) —
ver `docs/EMBED_GUIDE.md` para cómo se embebe en cada uno y por qué se
ubicó abajo-derecha (el sitio público ya tiene una burbuja de WhatsApp
abajo-izquierda).
