# Memoria técnica — Asistente Virtual RAG ISTTE

**Borrador de trabajo para Sprint 5 (21–27 jul 2026).**

Estructura genérica de memoria de titulación (Introducción / Marco teórico /
Metodología / Desarrollo / Resultados / Conclusiones). **Verificar contra el
formato oficial que exige la coordinación de titulación del ISTTE** — este
documento no lo reemplaza, es un punto de partida para no arrancar de cero.

Las secciones marcadas ✅ tienen contenido factual ya extraído del código y
los documentos del proyecto (arquitectura, decisiones ya tomadas). Las
marcadas 📝 son las que **tenés que escribir vos**: son justo las que te van
a preguntar en la defensa oral, así que no tiene sentido que las arme por
vos — union de eso depende que puedas explicarlas sin leer un papel.

---

## Capítulo 1 — Introducción 📝

Guía de lo que va acá (no el texto):
- Problema: ¿qué dificultad tienen hoy los estudiantes del ISTTE para
  encontrar información de reglamentos/trámites/calendarios?
- Justificación: ¿por qué un asistente conversacional y no, por ejemplo,
  mejorar el buscador de la web actual?
- Objetivo general y objetivos específicos (podés derivarlos de los 5
  sprints: entorno → ingesta → API/widget → evaluación/despliegue).
- Alcance: qué SÍ resuelve el asistente (dudas sobre reglamento, calendario,
  trámites) y qué NO (no reemplaza a secretaría, no hace trámites).

## Capítulo 2 — Marco teórico ✅ (borrador, revisar/ampliar)

### 2.1 RAG (Retrieval-Augmented Generation)
El asistente no usa un LLM "a secas": antes de generar la respuesta, busca
los fragmentos de texto más relevantes en una base vectorial (`ChromaDB`) y
se los pasa al modelo como contexto (`src/rag_chain.py`). Esto reduce las
alucinaciones frente a usar el LLM solo, porque la respuesta se ancla a
documentos reales del instituto en vez de depender de lo que el modelo
"recuerda" de su entrenamiento.

### 2.2 Componentes usados y por qué
- **Ollama + Llama 3.2**: modelo generativo corriendo local (no en la nube).
  Decisión de arquitectura: mantiene los datos del instituto (reglamentos,
  preguntas de estudiantes) dentro de la infraestructura propia, sin
  mandarlos a una API externa de terceros.
- **nomic-embed-text**: modelo de embeddings, también local vía Ollama,
  convierte cada fragmento de texto en un vector para poder buscar por
  similitud semántica (no por palabras exactas).
- **ChromaDB**: base de datos vectorial, persistida en disco
  (`chroma_db/`), evita recalcular los embeddings en cada consulta.
- **LangChain**: orquesta el pipeline (carga de PDFs, *chunking*,
  *retrieval*, armado del prompt) sin tener que escribir esa integración a
  mano contra cada componente.
- **FastAPI**: expone el pipeline como servicio HTTP (`POST /query`),
  desacoplado del frontend — así el mismo backend puede servir el widget
  embebido y, a futuro, otros clientes (app móvil, etc.).

*(📝 Si tu tutor pide comparar contra alternativas — ej. usar una API de LLM
en la nube en vez de Ollama local, o Pinecone/FAISS en vez de ChromaDB —
esa comparación y su justificación las tenés que redactar vos: son
decisiones de diseño que debés poder defender.)*

## Capítulo 3 — Metodología ✅ (borrador, revisar/ampliar)

Se usó **Scrum** con 5 sprints de 2 semanas (26 may – 27 jul 2026):

| Sprint | Fechas | Objetivo | Estado |
|--------|--------|----------|--------|
| 1 | 26 may – 08 jun | Entorno de desarrollo + recopilación de PDFs oficiales | Entorno listo; PDFs oficiales aún no entregados por secretaría |
| 2 | 09 jun – 22 jun | Pipeline de ingesta (`scripts/ingest.py`) + ChromaDB | Implementado y probado con PDFs de ejemplo |
| 3 | 23 jun – 06 jul | Endpoint `/query` (FastAPI) + widget de chat embebible | Completo |
| 4 | 07 jul – 20 jul | Evaluación con 30 consultas + despliegue en Render | Evaluación corrida (ver Cap. 4); despliegue real pendiente |
| 5 | 21 jul – 27 jul | Memoria técnica y defensa oral | En curso |

*(📝 Acá conviene explicar por qué Scrum y no cascada — por ejemplo, que el
proyecto dependía de un insumo externo incierto (los PDFs de secretaría) y
Scrum permitió seguir avanzando en paralelo con datos de ejemplo en vez de
bloquear todo el proyecto a la espera.)*

## Capítulo 4 — Desarrollo / Implementación 📝 (esqueleto con datos ✅)

Subsecciones sugeridas, una por componente construido:
1. Ingesta de documentos (`scripts/ingest.py`) — carga, *chunking* (700
   caracteres, 100 de solapamiento), generación de embeddings.
2. Cadena RAG (`src/rag_chain.py`) — *retrieval* (k=4) + *prompt* +
   generación.
3. API (`app/main.py`) — endpoint, CORS, manejo de errores.
4. Widget (`app/static/widget.html`) — UI del chat, consumo de la API.
5. Despliegue (`Dockerfile`, `render.yaml`) — ver `docs/DEPLOY_RENDER.md`.

Para cada uno: capturas de pantalla del código clave + explicación en tus
palabras de qué hace y qué decisiones tomaste (no solo "qué es" la
tecnología, que ya va en el Cap. 2).

## Capítulo 5 — Resultados y discusión 📝 (datos ✅, análisis pendiente)

Los datos crudos ya están en `docs/evaluacion/resultados_20260721_231922.md`
(30 consultas, 0 errores, ~3.02s de latencia promedio). **Importante:** esa
corrida fue contra los 2 PDFs de EJEMPLO — hay que volver a correr
`python scripts/evaluate.py` con los documentos oficiales del ISTTE antes
de que estos resultados sean válidos para la memoria final.

Dos hallazgos concretos de esa corrida que valen la pena discutir (son tuyos
para analizar, no los resuelvo yo):
- **Pregunta 18** ("¿Cuándo es la semana de exámenes finales?"): el sistema
  respondió "no tengo esa información" a pesar de que el dato SÍ está en
  `calendario_academico_ejemplo.pdf` y fue recuperado como fuente. Es un
  caso de *falso negativo* del modelo generativo, no del *retrieval*. ¿Por
  qué creés que pasa? (pista: temperatura del modelo, tamaño de k=4,
  ambigüedad del prompt). ¿Cómo lo medirías/mitigarías?
- **Pregunta 12**: la respuesta atribuye una fuente al "calendario
  académico" cuando el dato viene del reglamento (Art. 5). ¿Es un problema
  de *citación* (el LLM mezcla las fuentes en el texto libre) o de
  *retrieval* (trajo chunks de ambos documentos)? Esto es relevante para
  la fiabilidad del asistente: un estudiante que confíe en la fuente citada
  podría buscar en el documento equivocado.

Estructura sugerida: tabla resumen (latencia, tasa de error, tasa de
"no tengo información" para preguntas dentro vs. fuera de alcance) +
discusión de los dos casos de arriba + comparación con el objetivo de la
tesis (¿el asistente cumple lo que se propuso en el Cap. 1?).

## Capítulo 6 — Conclusiones y recomendaciones 📝

100% tuyo. Preguntas guía:
- ¿Se cumplieron los objetivos del Cap. 1? ¿Con qué limitaciones?
- Limitación más importante del proyecto tal como quedó: los PDFs oficiales
  del instituto nunca llegaron de secretaría, así que el sistema nunca fue
  evaluado con datos reales — ¿qué implica esto para las conclusiones que
  podés sacar honestamente?
- Limitación de arquitectura: Ollama local requiere una VM con RAM
  suficiente (ver `docs/DEPLOY_RENDER.md`) — ¿qué trade-off hiciste al
  elegir un LLM local en vez de una API en la nube?
- Trabajo futuro: ¿qué harías con más tiempo? (ej. reingesta con datos
  reales, métricas de evaluación más rigurosas tipo *precision@k*, feedback
  de usuarios reales del instituto)

---

## Para la defensa oral

Practicá poder explicar, sin mirar la memoria:
1. Qué es RAG y por qué se usó acá en vez de un LLM solo.
2. Por qué Ollama local y no una API en la nube (trade-off de datos/costo/RAM).
3. Qué es un *chunk* y por qué 700 caracteres con 100 de solapamiento.
4. El caso de la pregunta 18 (falso negativo) — es una pregunta muy probable
   del tribunal porque muestra que entendés las limitaciones reales de tu
   propio sistema, no solo que "funciona".
