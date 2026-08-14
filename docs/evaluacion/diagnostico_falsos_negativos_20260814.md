# Diagnóstico — falsos negativos con los PDFs oficiales

Fecha: 2026-08-14

> Nota: esto es evidencia cruda de una sesión de diagnóstico manual (no una
> corrida de `scripts/evaluate.py`). Sirve como insumo para el Capítulo 5
> de la memoria (ya tenías un caso similar con los PDFs de ejemplo —
> pregunta 18 de `docs/evaluacion/resultados_20260721_231922.md`). El
> análisis/discusión queda para vos, esto es solo el registro de lo que se
> probó y se observó.

## Contexto

Tras ingestar `matriz_roles_permisos_depurada.pdf` y
`videos_conocetuplataformaISTTE.pdf`, se probaron 4 preguntas sobre su
contenido real. 2 respondieron bien, 2 fallaron con "no tengo esa
información" a pesar de que el dato sí está en los documentos. Se investigó
cada falla por separado porque resultaron tener causas distintas.

## Caso 1 — "¿Cómo cambio mis datos de acceso a la plataforma EVA?"

**Causa: el chunk con la respuesta no entra en el top-k.**

`responder_pregunta` usa `k=4` (`src/rag_chain.py:38`). Se probó
`similarity_search_with_score` con `k=64` (todos los chunks) para ver en
qué posición queda el chunk que sí contiene el paso a paso de "Cambiar
contraseña":

| Rank (0-indexed) | Score (distancia) | Página | Contenido |
|---|---|---|---|
| 0 | 0.3572 | 0 | Introducción del video (autor, duración, tema general) |
| 1 | 0.4721 | 1 | Presentación general del Aula Virtual |
| 2 | 0.6128 | 2 | Otro procedimiento (entrega de tareas) |
| ... | ... | ... | ... |
| **10** | **0.7267** | **0** | **`### 4. Cambiar contraseña` — el paso a paso real** |

Con `k=4` solo entran los rank 0–3 al contexto del prompt; el chunk que
realmente responde la pregunta (rank 10) nunca llega al modelo. No es una
falla de generación — Llama 3.2 respondió correctamente sobre el contexto
incompleto que recibió.

Dato adicional: la página 0 del PDF se dividió en 4 chunks distintos por el
`chunk_size=700` de `scripts/ingest.py`, y el chunk "introductorio" (rank 0)
le gana en similitud al chunk con la respuesta real, aunque ese último es
el que el estudiante necesita.

## Caso 2 — "¿Qué permisos tiene el Docente Director de Proyecto?"

**Causa: coincidencia léxica, no de retrieval.**

Acá el chunk correcto sí venía en el contexto (confirmado con
`similarity_search`, rank 0 de 4). Para descartar que fuera un problema de
"ruido" por los otros 3 chunks del contexto, se aisló manualmente ese único
chunk y se volvió a invocar la cadena de generación (mismo
`PROMPT_TEMPLATE` de `src/rag_chain.py`):

- Contexto (aislado, sin otros chunks):
  > "Docente Director de Proyecto PostularInscribirSupervisarAprobar Horas.
  > Postula proyectos comunitarios completando perfil, justificación y plan
  > de aprendizaje. Inscribe a los estudiantes seleccionados, realiza el
  > seguimiento de las actividades en campo y valida el cumplimiento del
  > número de horas asignadas."

| Pregunta | Respuesta del modelo (mismo contexto) |
|---|---|
| "¿Qué **permisos** tiene el Docente Director de Proyecto?" | "No tengo información específica..." |
| "¿Qué **acciones** puede realizar el Docente Director de Proyecto?" | Lista correcta: postular, inscribir, hacer seguimiento, validar horas. |
| "¿Qué **hace** el Docente Director de Proyecto?" | "Supervisa y aprueba los proyectos comunitarios." (correcta, resumida) |

Cambiar solo la palabra clave de la pregunta (de "permisos" a "acciones"/
"hace") cambió el resultado de refuso→correcto **con el contexto
idéntico, sin tocar retrieval**. La palabra "permisos" no aparece en el
chunk (el PDF describe *acciones*: "Postular Inscribir Supervisar
Aprobar"), y el modelo pareció tratar eso como "el contexto no contiene la
respuesta" en vez de inferir que las acciones descritas SON los permisos.

## Para tu Capítulo 5 (preguntas guía, no las resuelvo yo)

- Caso 1 es un problema de **retrieval/chunking** (k muy chico, o chunks de
  700 caracteres demasiado finos para un procedimiento paso a paso). ¿Cómo
  lo medirías objetivamente (ej. recall@k sobre un set de preguntas con
  respuesta conocida)? ¿Qué trade-off tiene subir `k` o `chunk_size`
  (contexto más largo = más lento, más ruido para el modelo)?
- Caso 2 es un problema de **generación/prompt**, no de retrieval — el dato
  estaba disponible y el modelo lo descartó igual. ¿Es un límite del
  prompt actual ("responde ÚNICAMENTE con el contexto") siendo demasiado
  literal? ¿Cómo lo evaluarías sin simplemente "probar preguntas hasta que
  funcione" (que es lo que se hizo acá, de forma manual)?
- Ambos casos son útiles para contrastar con la Pregunta 18 ya documentada
  (que fue con datos de ejemplo): ahora tenés evidencia de que el mismo
  patrón de falso negativo aparece también con contenido real, con dos
  causas raíz distintas.
