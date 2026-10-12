# Estado real del código local — ISTTE-Bot

Revisado el 11/10/2026 sobre `C:\proyecto_istte\rag-istte-widget` (rama `master`, commit `5a6f083`, árbol de trabajo limpio antes de crear `entrega_tesis/`).

## 1. Parámetros actuales frente a los de la tesis

| Parámetro | Tesis | Código / datos locales | ¿Coincide? | Dónde está |
|---|---|---|---|---|
| k de recuperación | 8 | 8 | Sí | `src/rag_chain.py:97` (`responder_pregunta(pregunta, k=8)`) |
| chunk_size | 1200 | 1200 | Sí | `scripts/ingest.py:70` |
| chunk_overlap | 200 | 200 | Sí | `scripts/ingest.py:71` |
| Documentos del corpus | 5 | 5 | Sí | `data/reglamentos/` |
| Fragmentos en ChromaDB | 81 | **149 registros, 81 únicos** | **No del todo** | `chroma_db/` (ver sección 4) |
| Prompt del sistema | suavizado | suavizado | Sí | `src/rag_chain.py:32-37` |

Otros valores: modelo generativo `llama3.2`, embeddings `nomic-embed-text`, separadores del splitter `["\n\n", "\n", ". ", " ", ""]`, `PERSIST_DIR = "chroma_db"`.

## 2. Prompt del sistema (`SISTEMA_TEMPLATE`), texto completo

```text
Eres un asistente virtual del Instituto Superior Tecnologico Tecnoecuatoriano (ISTTE).
Responde la pregunta del estudiante usando UNICAMENTE la informacion del contexto que te
llega en el siguiente mensaje. Si el contexto menciona el tema de la pregunta, aunque sea
de forma parcial o indirecta, usa esa informacion para responder. Solo si el contexto no
menciona el tema en absoluto, di claramente que no tienes esa informacion y sugiere
consultar con secretaria academica. Responde en espanol, de forma breve y clara.
```

## 3. Documentos en `data/reglamentos/`

| Archivo | Tamaño (bytes) | Última modificación |
|---|---|---|
| GUÍA DEL DOCENTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf | 92 064 | 20/08/2026 |
| GUÍA DEL ESTUDIANTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf | 92 487 | 20/08/2026 |
| ISTTE_Catalogo_Procesos_Digitales.pdf | 42 305 | 14/08/2026 |
| matriz_roles_permisos_depurada.pdf | 33 083 | 14/08/2026 |
| videos_conocetuplataformaISTTE.pdf | 66 426 | 14/08/2026 |

Además hay un `.gitkeep`. Los 9 PDF excluidos (2 de ejemplo y 7 `EVA_*` personales) están en `data/_excluidos_evaluacion_oficial/`, carpeta ignorada por git.

## 4. Fragmentos en ChromaDB (contados sin reindexar)

Lectura directa de `chroma_db/` con `chromadb.PersistentClient` (colección `langchain`):

| Documento | Registros en el índice | Fragmentos únicos |
|---|---|---|
| ISTTE_Catalogo_Procesos_Digitales.pdf | 58 | 29 |
| videos_conocetuplataformaISTTE.pdf | 64 | 32 |
| matriz_roles_permisos_depurada.pdf | 14 | 7 |
| GUÍA DEL DOCENTE … P37.pdf | 7 | 7 |
| GUÍA DEL ESTUDIANTE … P37.pdf | 6 | 6 |
| **Total** | **149** | **81** |

- Los 81 fragmentos de la tesis son correctos como número de fragmentos **distintos**, pero el índice guarda 149 registros: los tres documentos originales están **duplicados** (cada fragmento aparece dos veces). `scripts/ingest.py` usa `Chroma.from_documents`, que añade al índice existente en vez de reemplazarlo, y la reingesta del 20/08 se hizo sobre un índice que ya tenía esos tres documentos.
- `chroma.sqlite3` se modificó por última vez el 20/08/2026 a las 18:16, cinco minutos antes de la corrida oficial (18:21). Es decir, **la corrida 2 se ejecutó contra este índice con duplicados**.
- Consecuencia para la tesis: con k=8, cuando los fragmentos recuperados son de los tres documentos duplicados, el modelo recibe en la práctica unos 4 fragmentos distintos repetidos dos veces. En el JSON de la corrida se ve el patrón: las fuentes aparecen casi siempre en pares. Conviene mencionarlo como limitación o repetir la evaluación con un índice limpio.
- Longitud máxima de fragmento en el índice: 1200 caracteres, coherente con `chunk_size=1200`.

Respaldos (ignorados por git): `chroma_db_backup_pre_chunk1200_20260818` (104 fragmentos, 3 documentos, corrida 1), `chroma_db_backup_12pdfs_20260818` (114) y `chroma_db_backup_20260818` (250).

## 5. Salidas de git

### `git status`

```text
On branch master
nothing to commit, working tree clean
```

(Tomada antes de crear `entrega_tesis/`. Ahora `git status --short` muestra `?? entrega_tesis/`.)

### `git log --oneline -5`

```text
5a6f083 Segunda corrida de evaluacion oficial (5 PDFs), informe tecnico y ajustes de memoria
7c0f9c2 Sacar PDFs personales del corpus, subir chunk_size/k y suavizar el prompt
d0368a8 Recrear qa/host_prueba.html como replica visual del sitio ISTTE
33c9eea Endurecimiento de seguridad: CORS fail-closed y usuario no-root en Docker
2b906e7 Responder saludos/charla casual sin pasar por retrieval
```

### `git branch -vv` y ramas remotas

```text
  main               3796031 [origin/main] Asistente Virtual RAG - ISTTE
* master             5a6f083 Segunda corrida de evaluacion oficial (5 PDFs), informe tecnico y ajustes de memoria
  prueba-ajustes-rag 33c9eea Endurecimiento de seguridad: CORS fail-closed y usuario no-root en Docker

  origin/HEAD -> origin/main
  origin/main
  origin/master
```

Remoto: `https://github.com/3rckan/rag-istte-widget.git`

### `git diff origin/main --stat`

```text
 .gitignore                                         |   5 +
 README.md                                          |   8 +-
 ...NTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf" | Bin 0 -> 92064 bytes
 ...NTE DE AULAS VIRTUALES (EVA) - PERIODO P37.pdf" | Bin 0 -> 92487 bytes
 data/reglamentos/calendario_academico_ejemplo.pdf  | Bin 1995 -> 0 bytes
 data/reglamentos/reglamento_academico_ejemplo.pdf  | Bin 2294 -> 0 bytes
 docs/PREGUNTAS_PRUEBA.md                           |  84 +++
 .../justificacion_metricas_tabla_tesis.md          | 285 ++++++++++
 .../resultados_oficiales_20260818_175610.json      | 452 ++++++++++++++++
 .../resultados_oficiales_20260820_182117.json      | 572 +++++++++++++++++++++
 docs/memoria/estructura_memoria.md                 |  28 +-
 docs/memoria/informe_tecnico_desarrollo.md         | 229 +++++++++
 qa/README.md                                       |  22 +-
 qa/assets/newlogotecno.png                         | Bin 0 -> 41207 bytes
 qa/host_prueba.html                                | 445 +++++++++++++++-
 qa/test_widget.py                                  |  32 +-
 scripts/evaluate_oficial.py                        | 146 ++++++
 scripts/ingest.py                                  |   4 +-
 src/rag_chain.py                                   |   9 +-
 19 files changed, 2270 insertions(+), 51 deletions(-)
```

### `git diff origin/master --stat`

```text
(sin salida: master local y origin/master son idénticos)
```

## 6. ¿Qué versión tiene GitHub?

| Rama | Commit | k | chunk | Prompt |
|---|---|---|---|---|
| `origin/main` (rama por defecto en GitHub) | `3796031` | 4 | 700 / 100 | estricto (versión vieja) |
| `origin/master` | `5a6f083` | 8 | 1200 / 200 | suavizado (versión final) |
| `master` local | `5a6f083` | 8 | 1200 / 200 | suavizado (versión final) |

- La versión final **ya está en GitHub**, pero en la rama `master`. Quien entre al repositorio ve por defecto `main`, que tiene la versión vieja.
- `origin/main` y `master` **no comparten historial**: `main` es un único commit independiente ("Asistente Virtual RAG - ISTTE") y `master` tiene 13 commits propios. No se puede actualizar `main` con un push normal; hace falta una fusión de historiales no relacionados, un push forzado o cambiar la rama por defecto en GitHub.

## 7. Revisión de archivos sensibles

`.gitignore` actual cubre: `venv/`, `__pycache__/`, `*.pyc`, `.env`, `chroma_db/`, `chroma_db_backup_*/`, `.DS_Store`, `*.log`, `.gstack/`, `data/_excluidos_evaluacion_oficial/`.

- `.env`: ignorado y nunca commiteado. Correcto.
- `chroma_db/` y sus respaldos: ignorados y nunca commiteados. Correcto.
- **PDF personales `EVA_*`: están en el historial de git.** Se añadieron en el commit `9a6d6de` y se borraron en `7c0f9c2`. Ya no están en la versión actual, pero siguen siendo recuperables desde el historial, y ese historial **ya está publicado** en `origin/master`. Si `main` se actualiza con el historial de `master`, también quedarán ahí.
- PDF rastreados en la versión actual: los 5 de `data/reglamentos/` (documentos institucionales). No se revisó su contenido en busca de datos personales.
- `entrega_tesis/` (nueva, sin rastrear): 3 Markdown y 3 PNG. Las capturas muestran la página de prueba `qa/host_prueba.html`, no el sitio oficial.

## 8. Otras diferencias menores entre código y documentación

- La cabecera de `scripts/evaluate_oficial.py` dice que las 30 preguntas se verificaron contra "los 3 PDFs institucionales"; el corpus actual tiene 5.
- Esa misma cabecera remite a `docs/evaluacion/justificacion_metricas_tabla.md`; el archivo real se llama `justificacion_metricas_tabla_tesis.md`.
- `SALUDO_SISTEMA_TEMPLATE` y el mensaje de bienvenida del widget invitan a preguntar por "reglamentos, calendarios o trámites", pero el corpus actual no contiene reglamentos ni calendarios.
- `CLAUDE.md` describe todavía el corpus como "2 PDFs de ejemplo".
