# Preguntas de prueba — qué puede responder el asistente ahora mismo

Este documento resume qué puede responder el asistente **con los datos
actualmente indexados** en `chroma_db/` (3 PDFs de `data/reglamentos/`,
68 chunks). Sirve como guía rápida para probar la burbuja a mano —
ver `docs/EMBED_GUIDE.md` para cómo levantarla en local.

**Estado:** actualizado el 2026-08-18, tras depurar el corpus a solo
contenido institucional real (se quitaron los 2 PDFs de ejemplo/ficticios
y los 7 `EVA_*.pdf` personales de Andrés — ver `docs/SETUP_PDFS.md`) y
reingestar con `chunk_size=1200`/`chunk_overlap=200` (antes 700/100).
Además se subió `k` de 4→8 y se suavizó `SISTEMA_TEMPLATE` en
`src/rag_chain.py` para que el modelo use el contexto aunque la mención
sea parcial/indirecta, en vez de negarse apenas no hay coincidencia
literal (bajó bastante la tasa de falsos negativos tipo "no tengo esa
información" con el dato presente en el contexto). Cambia en cuanto se
reingesten más PDFs oficiales del instituto (`python scripts/ingest.py`)
— ver `README.md` para el estado de cada sprint.

**Importante — Llama 3.2 no es determinista:** la misma pregunta, con el
mismo contexto recuperado, puede dar una respuesta correcta una vez y
"no tengo información" la siguiente (se midió ~75% de aciertos en 4
intentos seguidos de la misma pregunta). Si en una demo en vivo una
pregunta de la lista de abajo falla, repetirla suele bastar — no es que
se rompió el pipeline.

## Los 3 PDFs indexados

- `ISTTE_Catalogo_Procesos_Digitales.pdf` — contenido institucional real
  sacado del sitio web: admisión, matrícula, pagos, trámites en SIACAD,
  datos de contacto por sede/campus.
- `matriz_roles_permisos_depurada.pdf` — roles del sistema académico
  (Estudiante, Docente, Investigación, Vinculación, Gestión/Dirección,
  Técnico/Laboratorio) y qué puede hacer cada uno.
- `videos_conocetuplataformaISTTE.pdf` — tutorial de cómo cambiar datos
  de acceso (contraseña, perfil) en la plataforma EVA
  (`eva.tecnovirtual.edu.ec`).

## Preguntas verificadas para presentación/demo (probadas en vivo el 2026-08-18)

Estas se probaron contra el pipeline real (`responder_pregunta`, k=8,
prompt suavizado) y dieron respuesta útil y correcta — son las más
seguras para mostrar en vivo (recordar: repetir si alguna falla, ver
nota de no-determinismo arriba):

- ¿Qué trámites puedo hacer en línea?
- ¿Cómo me matriculo?
- ¿Cómo cambio mi contraseña en el EVA?
- ¿Cuál es el teléfono de la sede matriz?
- ¿Qué es la Biblioteca Virtual eLibro?
- ¿Qué es el correo institucional del estudiante?
- ¿Qué es el EVA? (~75% de aciertos, repetir si falla)
- ¿Cómo puedo sacar un certificado?
- ¿Cómo es la validación de conocimientos?

## Preguntas que NO puede responder bien (limitaciones conocidas — no usar en vivo)

- **"¿Cuál es el rol de un estudiante?" y preguntas de roles/permisos**
  (`matriz_roles_permisos_depurada.pdf`). El chunk que define cada rol
  (tabla "Actor / Rol") queda muy abajo en el ranking de similitud (ej.
  rank 49 de 68 para "rol de un estudiante") porque es una tabla con
  mucho texto de encabezado/metadata que diluye el embedding — ni
  subiendo k a un valor razonable entra al contexto. Ver también Caso 2
  de `docs/evaluacion/diagnostico_falsos_negativos_20260814.md`. Evitar
  este tipo de pregunta en una demo en vivo.
- **"¿Cuál es la escala de calificaciones?"** — este dato genuinamente
  NO está en ningún PDF del corpus (solo se menciona "Escalafón
  Docente", que es otra cosa). El rechazo acá es correcto, no un bug.
- **Horarios de clases y calendario académico.** No hay ningún PDF con
  horarios reales — el único PDF que alguna vez cubrió esto
  (`calendario_academico_ejemplo.pdf`) era un dato ficticio y ya se quitó
  del corpus. El catálogo de procesos sí menciona que el horario de
  materias se consulta en SIACAD (`ACADÉMICO > BÚSQUEDAS > Buscar
  Planificación de Materias`), pero el retrieval no lo trae al top-k para
  preguntas casuales tipo "en qué horario son las clases" — el chunk
  correcto queda en el rank ~47 de 68 (mismo patrón de falso negativo que
  los Casos 1 y 2 de `docs/evaluacion/diagnostico_falsos_negativos_20260814.md`,
  aún sin agregar ahí como caso aparte).
- Mallas curriculares, becas, o cualquier reglamento académico real (los
  oficiales siguen pendientes de secretaría, ver `README.md`).
- Preguntas sobre cursos personales de Andrés (`EVA_*.pdf`) — esos PDFs
  se sacaron del corpus a propósito por ser datos personales, no
  institucionales, y además degradan el retrieval de horarios/calendario
  (ver detalle en memoria del asistente, `rag_widget_eva_personal_pdfs`).
