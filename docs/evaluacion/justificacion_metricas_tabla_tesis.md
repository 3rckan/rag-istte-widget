# Justificación metodológica de la tabla de evaluación del asistente RAG-ISTTE

**Proyecto:** Sistema de direccionamiento estudiantil basado en RAG — ISTTE
**Autor:** Andrés Guachamin
**Fecha de la corrida:** 2026-08-18
**Trazabilidad:** `scripts/evaluate_oficial.py` → `docs/evaluacion/resultados_oficiales_20260818_175610.json`

## 1. Objetivo

Este documento respalda la tabla de resultados del capítulo de evaluación de
la memoria técnica. Reemplaza una versión anterior de la tabla cuyas cifras
no pudieron trazarse a una corrida reproducible contra el pipeline actual;
los valores de esta versión sí están respaldados por un script versionado,
un set de preguntas con respuesta verificada contra el texto fuente, y el
JSON crudo con cada respuesta del modelo.

## 2. Corpus utilizado

La evaluación oficial se corrió **únicamente** contra los 3 documentos
institucionales reales del ISTTE que forman parte legítima del corpus de
producción:

- `ISTTE_Catalogo_Procesos_Digitales.pdf` — catálogo de trámites y
  plataformas digitales, extraído del sitio oficial istte.edu.ec.
- `matriz_roles_permisos_depurada.pdf` — matriz de roles, permisos y
  funcionalidades del sistema académico.
- `videos_conocetuplataformaISTTE.pdf` — transcripciones/descripciones de
  tutoriales en video sobre el uso de EVA, SIACAD, correo y biblioteca
  virtual.

Se excluyeron explícitamente del corpus de evaluación (movidos a
`data/_excluidos_evaluacion_oficial/`, no borrados):

- Los 2 PDFs de ejemplo (`reglamento_academico_ejemplo.pdf`,
  `calendario_academico_ejemplo.pdf`) del Sprint 2/3, que contienen
  reglamentos ficticios usados solo para validar el pipeline en desarrollo.
- Los 7 PDFs `EVA_*.pdf`, que son exportaciones de los cursos personales del
  autor en la plataforma EVA (datos personales, no reglamentos
  institucionales) — nunca estuvieron destinados a producción.

Con el corpus depurado se volvió a correr `scripts/ingest.py`, generando un
índice nuevo de 104 fragmentos en ChromaDB.

## 3. Metodología / rúbrica de evaluación

`scripts/evaluate_oficial.py` define 30 preguntas con una respuesta esperada
(`"esperado"`) verificada manualmente contra el texto extraído de los 3 PDF
reales (no contra suposiciones). Cada pregunta se ejecutó una vez contra el
pipeline real (`responder_pregunta`, retrieval con ChromaDB + generación con
Llama 3.2 vía Ollama), registrando respuesta, fuentes recuperadas y tiempo.

El scoring de cada respuesta se hizo con dos criterios binarios aplicados
por separado, uno por pregunta:

- **Precisión semántica** (solo sobre las 24 preguntas "en dominio" o
  "combinadas", IDs 1–24): ¿la respuesta transmite correctamente el hecho
  clave de `esperado`? Un rechazo ("no tengo esa información") cuando el
  dato sí existe en el corpus cuenta como **incorrecto** (falso negativo).
- **Fidelidad a la fuente** (las 30 preguntas): ¿todo lo afirmado en la
  respuesta es atribuible correctamente al fragmento fuente, sin mezclar
  datos de una entidad/sistema con otro? Una respuesta que cita texto real
  del corpus pero lo atribuye a la entidad equivocada (p. ej. el botón de
  un sistema aplicado a otro) cuenta como **no fiel**, aunque las palabras
  existan en el corpus — el criterio es la atribución correcta, no solo la
  presencia literal del texto.
- **Respuestas fuera de dominio** (4 preguntas, IDs 25–28): ¿el asistente
  rechazó correctamente responder en vez de inventar una respuesta?

Este scoring lo hizo Claude (Sonnet 5) leyendo el texto completo de los 3
PDF y comparando cada una de las 30 respuestas contra él, incluyendo
verificación cruzada por búsqueda de texto exacto para descartar falsos
positivos de alucinación (ver sección 5.2, casos 21 y 22).

## 4. Resultados

| Métrica | Criterio de aceptación | Resultado obtenido |
|---|---|---|
| Precisión semántica | > 85.0% | **50.0%** (12/24) |
| Fidelidad a la fuente | > 90.0% | **83.3%** (25/30) |
| Respuestas fuera de dominio | 100.0% rechazo | **100.0%** (4/4) |
| Tiempo de respuesta | < 4.00 s | **7.88 s** (promedio, CPU local) |

De las 4 métricas, solo **respuestas fuera de dominio** cumple el criterio
de aceptación. Las otras 3 no lo cumplen con la configuración actual del
pipeline (k=4, `chunk_size=700`, prompt estrictamente literal, inferencia
sobre CPU).

## 5. Análisis por métrica

### 5.1 Precisión semántica (50.0%) — dominada por falsos negativos

8 de las 12 respuestas incorrectas son **falsos negativos**: el modelo
responde "no tengo esa información" cuando el dato sí está en el corpus
recuperado o en el corpus completo. Ejemplo (pregunta 7):

> **Pregunta:** ¿Qué módulos están disponibles en el SIACAD tras iniciar
> sesión?
> **Esperado:** Académico, Investigación, Vinculación, PPP, Reportes y
> Configuración (texto literal en `ISTTE_Catalogo_Procesos_Digitales.pdf`,
> sección 2.1).
> **Respuesta del modelo:** "No tengo esa información. Sugiero consultar
> con la Secretaria Académica."

Esta causa raíz ya había sido diagnosticada el 2026-08-14 en
`docs/evaluacion/diagnostico_falsos_negativos_20260814.md`: con `k=4`
(`src/rag_chain.py`), el fragmento correcto a veces queda fuera del top-4
por similitud de embeddings, o el prompt ("responde ÚNICAMENTE con el
contexto") hace que el modelo trate paráfrasis razonables como "el contexto
no contiene la respuesta". Esta corrida cuantifica por primera vez el
impacto real de ese problema conocido sobre un set de preguntas de dominio:
33% de las preguntas en dominio (8/24) lo sufren.

Las otras 4 incorrectas son **conflaciones**: el modelo mezcla datos de dos
entidades/secciones similares del corpus (ver 5.2).

### 5.2 Fidelidad a la fuente (83.3%) — contaminación cruzada entre secciones parecidas

5 de las 30 respuestas presentan información real del corpus pero atribuida
a la entidad equivocada, típicamente porque el retrieval trae fragmentos de
dos secciones estructuralmente parecidas (dos sistemas, dos roles) y el
modelo las combina:

- **Pregunta 15** ("¿botón para guardar el cambio de contraseña en EVA?"):
  el modelo respondió "Cambiar contraseña" — ese es el nombre del botón en
  **SIACAD**, no en EVA (cuyo botón real es "Guardar cambios"). Ambos
  procedimientos están en el mismo PDF de tutoriales.
- **Pregunta 20** ("¿usuario para iniciar sesión en SIACAD?"): el modelo
  respondió con el formato de correo institucional (`nombre.apellido@
  tecnovirtual.edu.ec`), que corresponde al login del **Webmail**, no al de
  SIACAD (que usa el número de cédula).
- **Pregunta 11 y 24**: el modelo mezcla las descripciones de roles
  parecidos en `matriz_roles_permisos_depurada.pdf` (p. ej. "Docente
  Director de Proyecto" de Vinculación con roles de Investigación).

Nota metodológica importante: al verificar dos casos que en un primer
scoring se habían marcado como alucinación pura (preguntas 21 y 22), una
búsqueda de texto exacto sobre los 3 PDF mostró que **ambas respuestas del
modelo sí están respaldadas literalmente por el corpus** — lo que ocurre es
que el corpus mismo tiene información inconsistente entre el catálogo
institucional y las descripciones de video (p. ej. el catálogo dice que el
correo estudiantil usa el dominio `red360.net`, mientras un tutorial en
video usa como ejemplo `@tecnovirtual.edu.ec`). Esas 2 preguntas se
recalificaron como correctas/fieles tras la verificación. Esto es en sí un
hallazgo relevante: parte del "error" medible no es del pipeline sino de
inconsistencias en las fuentes documentales usadas para construir el
corpus.

### 5.3 Respuestas fuera de dominio (100.0%) — único criterio que se cumple

Las 4 preguntas sin respuesta en el corpus (costo de pensión regular, rector
actual, contraseña de WiFi, clima) fueron rechazadas correctamente en las 4
ocasiones, sin inventar información. El manejo de preguntas ambiguas (IDs
29–30, no contabilizadas en esta métrica) fue mixto: la pregunta de una sola
palabra ("notas") sí generó una respuesta con datos combinados
incorrectamente, mientras que una cadena sin sentido ("asdkjaslkdj") se
rechazó apropiadamente.

### 5.4 Tiempo de respuesta (7.88 s) — no cumple, esperable en CPU

El promedio real sobre 30 consultas fue 7.88 s, muy por encima del criterio
de 4.00 s. Esto es consistente con correr Llama 3.2 vía Ollama sobre CPU
local (sin GPU dedicada) — no es un problema de lógica del pipeline sino de
la infraestructura de inferencia usada durante el desarrollo.

## 6. Limitaciones de este estudio

- El set de 30 preguntas es de tamaño moderado; los porcentajes tienen
  granularidad de ~4 puntos por pregunta (1/24, 1/30).
- El scoring de precisión/fidelidad fue hecho por un evaluador único
  (asistido por IA, sin doble revisión ciega ni panel de jueces), lo cual es
  una limitación reconocida para trabajos de titulación — se recomienda
  mencionarlo explícitamente como amenaza a la validez en el capítulo de
  metodología.
- El corpus real disponible al momento de esta evaluación es parcial (3
  documentos) comparado con el catálogo completo de trámites del instituto;
  los resultados no deben generalizarse como el desempeño final del sistema
  en producción con el corpus completo.

## 7. Recomendación

Antes de reportar estas cifras como definitivas en la memoria, se recomienda
intentar al menos una iteración de mejora sobre las causas raíz identificadas
(subir `k`, aumentar `chunk_size` o solapamiento entre chunks, y suavizar la
instrucción del prompt para permitir inferencia razonable sobre el contexto
recuperado) y volver a correr `scripts/evaluate_oficial.py` para verificar
si las métricas se acercan a los criterios de aceptación. El script y el set
de preguntas quedan versionados para que la corrida sea reproducible en
cualquier momento.
