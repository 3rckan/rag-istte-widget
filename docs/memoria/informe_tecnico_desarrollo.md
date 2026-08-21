# Informe técnico — Desarrollo y evaluación del Asistente RAG-ISTTE

**Material de referencia factual para la memoria de titulación.**
Última actualización: 2026-08-20.

> Este documento reúne hechos verificables del proyecto (arquitectura,
> decisiones de datos, metodología, resultados de evaluación) para que los
> uses como base al redactar tu memoria. **No es un capítulo redactado en
> tu voz ni contiene análisis/discusión/conclusiones** — eso corresponde a
> los capítulos 1, 5 (discusión) y 6 de `docs/memoria/estructura_memoria.md`,
> que son trabajo tuyo. Todo lo de acá tiene su fuente citada (archivo,
> línea, o documento) para que puedas verificarlo vos mismo.

---

## 1. Arquitectura del sistema

Servicio desacoplado: backend API (FastAPI) independiente + widget de chat
embebible.

| Componente | Tecnología | Rol |
|---|---|---|
| Modelo generativo | Llama 3.2 vía Ollama (local) | Genera la respuesta en lenguaje natural a partir del contexto recuperado |
| Embeddings | nomic-embed-text vía Ollama (local) | Convierte cada fragmento de texto y cada pregunta en un vector para búsqueda semántica |
| Base vectorial | ChromaDB, persistida en `chroma_db/` | Almacena los fragmentos indexados y resuelve la búsqueda por similitud |
| Orquestación | LangChain | Encadena carga de PDF → *chunking* → *retrieval* → *prompt* → generación |
| API | FastAPI (`app/main.py`) | Expone `POST /query`; CORS configurable por `ALLOWED_ORIGINS` |
| Frontend | `app/static/widget.html` + `widget-loader.js` | Burbuja de chat embebible vía iframe + script único |

**Decisión de arquitectura — LLM y embeddings 100% locales (Ollama), no
una API en la nube:** mantiene los datos del instituto (contenido de los
reglamentos, preguntas de los estudiantes) dentro de infraestructura
propia en vez de enviarlos a un tercero. Contrapartida medida: latencia
de 7–9s por respuesta corriendo sobre CPU (sección 5).

## 2. Pipeline RAG — configuración actual

Fuente: `scripts/ingest.py`, `src/rag_chain.py` (commit `7c0f9c2` en adelante).

| Parámetro | Valor actual | Valor original (Sprint 2) |
|---|---|---|
| `chunk_size` | 1200 caracteres | 700 |
| `chunk_overlap` | 200 caracteres | 100 |
| `k` (fragmentos recuperados por consulta) | 8 | 4 |
| Prompt del sistema | Instruye a usar el contexto si menciona el tema aunque sea parcial/indirecto; solo rechaza si el tema no aparece en absoluto | Instruía a rechazar ante cualquier no-coincidencia literal |

Los tres cambios (`chunk_size`/`overlap`, `k`, prompt) se aplicaron el
2026-08-20 como iteración sobre causas raíz identificadas en la primera
evaluación oficial (sección 5). El detalle de la motivación de cada
cambio está en `docs/evaluacion/justificacion_metricas_tabla_tesis.md`,
sección 8.

Detección de saludo/charla casual (`_es_saludo_o_charla`,
`src/rag_chain.py:81`): se resuelve por coincidencia de patrones de texto,
sin pasar por el LLM ni por retrieval. Motivo documentado en el código: la
misma pregunta ("hola") a veces se respondía bien y a veces se rechazaba
con "no tengo información" cuando se delegaba esa decisión al modelo — es
la primera evidencia registrada de la no-determinicidad de Llama 3.2 que
se cuantifica más adelante (sección 5.4).

## 3. Corpus de datos: composición y gobernanza

### 3.1 Composición actual (`data/reglamentos/`, 5 PDFs, 81 fragmentos)

| Documento | Naturaleza |
|---|---|
| `ISTTE_Catalogo_Procesos_Digitales.pdf` | Contenido institucional real, extraído del sitio web oficial |
| `matriz_roles_permisos_depurada.pdf` | Matriz de roles y permisos del sistema académico |
| `videos_conocetuplataformaISTTE.pdf` | Transcripciones de tutoriales sobre EVA, SIACAD, correo y biblioteca |
| `GUÍA DEL DOCENTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf` | Guía institucional real, agregada 2026-08-20 |
| `GUÍA DEL ESTUDIANTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf` | Guía institucional real, agregada 2026-08-20 |

### 3.2 Datos excluidos deliberadamente (`data/_excluidos_evaluacion_oficial/`)

- **2 PDFs de ejemplo/ficticios** (`reglamento_academico_ejemplo.pdf`,
  `calendario_academico_ejemplo.pdf`, del Sprint 2): contienen normativa
  simulada, no real. Se excluyeron para que el asistente no le presente a
  un estudiante fechas o reglas inventadas como si fueran del ISTTE real.
- **7 PDFs `EVA_*.pdf`**: exportaciones de los cursos personales del autor
  en la plataforma EVA (progreso académico individual, no reglamentos
  institucionales). Se excluyeron por dos motivos verificados de forma
  independiente:
  1. Son datos personales del autor, no información institucional que
     deba responderse a cualquier estudiante.
  2. Se midió empíricamente que degradan el *retrieval*: fragmentos como
     "Registro de clases (mayo 2026): Clase 11-05-26, 12-05-26..." repiten
     la palabra "clases" con alta densidad y desplazan en el ranking de
     similitud a los fragmentos que sí responden preguntas reales de
     calendario (un caso medido: el fragmento correcto pasó del *rank* 99
     de 114 cuando estos PDFs estaban incluidos).

Los archivos no se borraron, solo se movieron — están disponibles si se
necesitan para otro propósito (ej. una demo interna), pero fuera del
corpus de evaluación oficial y de producción.

## 4. Metodología de evaluación

Fuente: `scripts/evaluate_oficial.py`.

- 30 preguntas con respuesta esperada verificada manualmente contra el
  texto extraído de los PDF (no contra suposiciones), en 5 categorías:
  22 "en dominio", 2 "combinadas" (requieren relacionar dos partes del
  corpus), 4 "fuera de dominio" (el corpus no tiene la respuesta), 2
  "ambiguas" (una palabra suelta, una cadena sin sentido).
- Cada pregunta se ejecuta una vez contra el pipeline real
  (`responder_pregunta`), registrando respuesta, fuentes recuperadas y
  tiempo.
- El *scoring* (correcto/incorrecto, fiel/no fiel a la fuente) se hace
  después, leyendo el texto completo de los PDF y comparando cada
  respuesta — no es automático. Metodología completa y rúbrica en
  `docs/evaluacion/justificacion_metricas_tabla_tesis.md`, sección 3.

**Limitación metodológica reconocida:** el *scoring* lo hizo un solo
evaluador (asistido por IA), sin doble revisión ciega ni panel de jueces
— amenaza a la validez que conviene declarar explícitamente en el
capítulo de metodología de la memoria.

## 5. Resultados de evaluación

### 5.1 Tabla comparativa

| Métrica | Criterio de aceptación | Tabla original de la tesis (no trazable a una corrida real) | Corrida 1 — 2026-08-18 (3 PDFs) | Corrida 2 — 2026-08-20 (5 PDFs, tras iterar) |
|---|---|---|---|---|
| Precisión semántica | > 85.0% | 93.3% | 50.0% (12/24) | 58.3% (14/24) |
| Fidelidad a la fuente | > 90.0% | 96.6% | 83.3% (25/30) | 86.7% (26/30) |
| Respuestas fuera de dominio manejadas bien | 100.0% | 100.0% | 100.0% (4/4) | 100.0% (4/4) |
| Tiempo de respuesta promedio | < 4.00 s | 2.15 s | 7.88 s | 8.85 s |

Ninguna de las dos corridas reales cumple los criterios de precisión,
fidelidad o tiempo. La tabla original no pudo trazarse a ningún script o
JSON reproducible del repositorio.

### 5.2 Causas raíz identificadas (con evidencia)

**a) Falsos negativos por retrieval insuficiente en contenido tabular.**
El caso más consistente entre ambas corridas: 4 preguntas sobre
`matriz_roles_permisos_depurada.pdf` (qué rol hace tal función) fallan en
las dos corridas con "no tengo información", aunque el dato está en el
PDF. Verificado con `similarity_search_with_score(k=68)`: el fragmento
correcto (una tabla con mucho texto de encabezado/metadata) queda en
posiciones tan bajas como el *rank* 49 de 68 — ni subiendo `k` a un valor
razonable entra al contexto. Es un problema de *chunking* semántico sobre
contenido tabular, no de generación.

**b) Contaminación cruzada entre secciones estructuralmente parecidas.**
El modelo mezcla datos de dos entidades/sistemas similares cuando ambos
aparecen en el contexto recuperado. Ejemplos verificados: atribuyó el
botón "Cambiar contraseña" (de SIACAD) a una pregunta sobre EVA (cuyo
botón real es "Guardar cambios"); en la corrida 2, presentó una lista de
sub-opciones de un submenú de SIACAD como si fuera la lista completa de
módulos del sistema.

**c) Inconsistencias dentro del propio corpus documental.** Al menos un
caso verificado por búsqueda de texto exacto: el catálogo institucional
usa `red360.net` como dominio de correo estudiantil de ejemplo, un
tutorial en video usa `@tecnovirtual.edu.ec`. Una respuesta que cite
cualquiera de los dos está "respaldada por el corpus" pero puede leerse
como incorrecta si se compara contra el otro documento — el corpus mismo
tiene datos contradictorios entre fuentes.

**d) Alucinación con contexto ambiguo.** Distinto de (c): en la corrida 2,
una pregunta sobre el dominio de correo estudiantil obtuvo una respuesta
(`tecnoecuatoriano.edu.ec`) que no coincide con **ninguna** de las fuentes
reales del corpus — no es una inconsistencia heredada del corpus, es
información nueva inventada por el modelo.

### 5.3 Trade-off medido al suavizar el prompt (2026-08-20)

Subir `k` y suavizar el prompt (sección 2) redujo los falsos negativos de
tipo (b)/(c) pero no los de tipo (a) —las 4 preguntas de roles/permisos
siguen fallando igual en ambas corridas—, y coincide con la aparición del
patrón (d): dos respuestas incorrectas presentadas *sin* la señal de "no
tengo información" que antes alertaba de una posible falla. Es un
trade-off real y medido, no solo teórico: menos rechazos injustificados a
cambio de más riesgo de una respuesta incorrecta confiada cuando el
contexto es ambiguo.

### 5.4 No determinismo del modelo local

Verificado repitiendo la misma pregunta ("¿qué es el EVA?") 4 veces
seguidas con el mismo contexto recuperado: 3 respuestas correctas, 1
incorrecta (75% de consistencia). Las preguntas 15 y 20 del set de
evaluación fallan en ambas corridas oficiales, pero con **errores
distintos** cada vez — evidencia adicional de que Llama 3.2, corriendo
localmente vía Ollama, no produce la misma respuesta de forma consistente
ante el mismo contexto.

## 6. Limitaciones conocidas del sistema en su estado actual

- El corpus institucional real es parcial (5 documentos): los reglamentos
  y calendarios académicos oficiales de secretaría no forman parte del
  corpus a la fecha de este informe.
- El *retrieval* sobre contenido tabular (roles y permisos) es el cuello
  de botella individual más importante identificado — no resuelto por los
  ajustes de `k`/`chunk_size`/prompt.
- El tiempo de respuesta (7.9–8.9 s promedio) no cumple el criterio de
  aceptación (< 4.00 s); es atribuible a correr Llama 3.2 sobre CPU local
  sin GPU, no a la lógica del pipeline.
- El modelo no es determinista: la misma pregunta, con el mismo contexto,
  puede responderse correctamente una vez y de forma incorrecta la
  siguiente.
- Despliegue real en Render.com pendiente — requiere plan de pago con RAM
  suficiente para correr Ollama (ver `docs/DEPLOY_RENDER.md`).

## 7. Trazabilidad

- Scripts: `scripts/ingest.py`, `scripts/evaluate_oficial.py`,
  `src/rag_chain.py`.
- Resultados crudos (JSON): `docs/evaluacion/resultados_oficiales_20260818_175610.json`,
  `docs/evaluacion/resultados_oficiales_20260820_182117.json`.
- Metodología y scoring detallado: `docs/evaluacion/justificacion_metricas_tabla_tesis.md`.
- Diagnóstico previo de falsos negativos (2026-08-14):
  `docs/evaluacion/diagnostico_falsos_negativos_20260814.md`.

---

## Lo que este informe deliberadamente NO incluye

Por diseño (ver nota al inicio y `docs/memoria/estructura_memoria.md`):

- **Justificación/motivación del proyecto** (Cap. 1) — por qué un
  asistente conversacional resuelve un problema real de los estudiantes.
- **Discusión interpretativa de qué significan estos resultados** para el
  objetivo de la tesis (Cap. 5) — los datos de la sección 5 son la
  materia prima, la interpretación es tuya.
- **Conclusiones y trabajo futuro** (Cap. 6).

Son las secciones que un tribunal va a esperar que puedas defender con
tus propias palabras, no leyendo un documento generado.
