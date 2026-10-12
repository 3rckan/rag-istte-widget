# Anexo 2. Banco de 30 consultas de evaluación

**Fuente de las consultas y respuestas esperadas:** `scripts/evaluate_oficial.py`
**Fuente de las respuestas del sistema (corrida 2):** `docs/evaluacion/resultados_oficiales_20260820_182117.json` (20/08/2026, 18:21)
**Fuente de las marcas de precisión y fidelidad:** `docs/evaluacion/justificacion_metricas_tabla_tesis.md`, sección 8 (segunda corrida)

> **Aviso sobre las marcas.** En el repositorio **no existe una tabla de scoring pregunta por pregunta**
> de la corrida 2. El JSON no guarda marcas, y el documento de justificación solo registra los totales
> y nombra algunas preguntas concretas. Por eso las columnas de precisión y fidelidad solo llevan ✔/✘
> donde el documento lo dice de forma expresa; el resto figura como "sin registro". Ver el detalle al final.

| N.° | Categoría | Consulta | Respuesta esperada | Respuesta del sistema (corrida 2, resumida) | Precisión | Fidelidad |
|---|---|---|---|---|---|---|
| 1 | dominio | ¿Cuál es el correo institucional general de contacto del ISTTE? | info@istte.edu.ec | El correo institucional general de contacto es info@istte.edu.ec. | sin registro | sin registro |
| 2 | dominio | ¿Cuál es el costo del proceso de validación de conocimientos y experiencia para ingresar a una carrera? | $2600, con opción de pago de contado, tarjeta de crédito, u 8 pagos mensuales | El costo del proceso de validación es de $2600 (no menciona las formas de pago). | sin registro | sin registro |
| 3 | dominio | ¿Cuántos años de edad debe tener un aspirante para el proceso de validación de conocimientos y experiencia? | 25 años o más | Indica que no tiene información sobre la edad mínima y sugiere consultar con Secretaría Académica. | sin registro | sin registro |
| 4 | dominio | ¿Cuál es el enlace del portal de empleo del ISTTE? | https://portalempleo.istte.edu.ec/ | El enlace es https://portalempleo.istte.edu.ec/. | sin registro | sin registro |
| 5 | dominio | ¿Cuál es el horario de atención de la Sede Matriz (La Magdalena)? | Lunes a viernes, 8:00 a 19:00 | El horario es de lunes a viernes de 8:00 a 19:00. | sin registro | sin registro |
| 6 | dominio | ¿Qué documento relacionado a salud se pide en PDF antes de iniciar las Prácticas Preprofesionales? | Carnet de vacunación COVID-19 (y para carreras de Salud y Bienestar, vacunas de hepatitis B y tétanos) | Copia a color de vacunas de hepatitis B y tétanos en PDF, junto con cédula y papeleta de votación (no menciona COVID-19). | sin registro | sin registro |
| 7 | dominio | ¿Qué módulos están disponibles en el SIACAD tras iniciar sesión? | Académico, Investigación, Vinculación, PPP, Reportes y Configuración | Lista Auto Inscripción, Auto Matriculación y Pago de la Auto Matrícula como si fueran los módulos. | ✘ | sin registro ¹ |
| 8 | dominio | ¿Qué información muestra el reporte de Notas y Asistencias de un estudiante en SIACAD? | Promedio (GPA), créditos aprobados, y detalle de notas y porcentaje de asistencia por materia y nivel, con el docente responsable | Promedio (GPA), créditos aprobados, notas y porcentaje de asistencia por materia y nivel, estado y docente responsable. | sin registro | sin registro |
| 9 | dominio | ¿Qué rol se encarga de tomar la asistencia diaria y registrar notas parciales de los estudiantes? | Docente | Indica que no tiene información específica sobre ese rol y sugiere consultar con Secretaría Académica. | ✘ | sin registro |
| 10 | dominio | ¿Quién aprueba la emisión de certificados e informes finales de investigación? | Gestión de Investigación | "No tengo esa información. Sugiero consultar con la Secretaría Académica." | ✘ | sin registro |
| 11 | dominio | ¿Qué acciones puede realizar el Docente Director de Proyecto en Vinculación con la Sociedad? | Postular proyectos, inscribir estudiantes, supervisar el seguimiento en campo y aprobar el cumplimiento de horas | Postular proyectos comunitarios, inscribir estudiantes, dar seguimiento en campo y validar horas; añade que aprueba la inscripción de estudiantes. | sin registro | sin registro |
| 12 | dominio | ¿Quién administra el uso de talleres, laboratorios y equipos informáticos, y reporta incidencias técnicas? | Técnico de Laboratorio | El técnico de laboratorio gestiona talleres, laboratorios y equipos, y reporta mantenimientos, insumos e incidencias técnicas. | sin registro | sin registro |
| 13 | dominio | ¿Qué rol brinda seguimiento a estudiantes con Necesidades Educativas Especiales (NEE)? | Docente y Bienestar Estudiantil (UBE) | Indica que no tiene información específica sobre ese rol y recomienda consultar con Secretaría Académica. | ✘ | sin registro |
| 14 | dominio | ¿Cuáles son los campos obligatorios para cambiar la contraseña en la plataforma EVA? | Contraseña actual, nueva contraseña y confirmar nueva contraseña | Contraseña actual, nueva contraseña y confirmar nueva contraseña. | sin registro | sin registro |
| 15 | dominio | ¿Cuál es el nombre del botón para guardar los cambios al cambiar la contraseña en EVA? | "Guardar cambios" | Responde que el botón se llama "Cambiar contraseña". | ✘ | sin registro ² |
| 16 | dominio | ¿Qué formato de archivo se recomienda usar al enviar una tarea en la plataforma EVA? | PDF | Se recomienda usar formato PDF. | sin registro | sin registro |
| 17 | dominio | ¿Cuál es el tamaño máximo permitido para adjuntar un archivo al enviar un correo institucional? | 50 MB | El tamaño máximo es de 50 MB. | sin registro | sin registro |
| 18 | dominio | ¿Qué plataforma externa se usa para la biblioteca virtual del instituto? | eLibro (elibro.net) | eLibro, con la URL https://elibro.net/es/lc/istte/inicio. | sin registro | sin registro |
| 19 | dominio | ¿Cuál es la regla para formar la contraseña inicial de acceso a la biblioteca virtual eLibro? | Número de cédula del estudiante + primera letra del nombre en minúscula | Correo institucional como usuario; contraseña: número de cédula + primera letra del nombre en minúscula. | sin registro | sin registro |
| 20 | dominio | ¿Qué se usa como nombre de usuario para iniciar sesión en el SIACAD? | El número de cédula del estudiante | Indica que no tiene información específica sobre el nombre de usuario y sugiere consultar con Secretaría Académica. | ✘ | sin registro |
| 21 | dominio | ¿Qué opciones aparecen dentro del menú 'Búsquedas' del SIACAD? | Buscar evaluación al docente, y Buscar Matrículas | Dos opciones: Buscar evaluación al docente y Buscar Matrículas. | sin registro | sin registro |
| 22 | dominio | ¿Cuál es el dominio de correo institucional que usan los estudiantes del Tecnoecuatoriano? | @tecnovirtual.edu.ec | Responde que el dominio es tecnoecuatoriano.edu.ec, igual al del sitio web oficial. | ✘ | ✘ |
| 23 | combinada | Si quiero saber mis notas y mi porcentaje de asistencia, ¿en qué sistema y en qué reporte lo encuentro? | En el SIACAD, en el reporte de Notas y Asistencias (Reportes > Notas y Asistencias Alumnos) | En el SIACAD, menú "Reportes", opción "Notas y Asistencias Alumnos". | sin registro | sin registro |
| 24 | combinada | Como estudiante, ¿ante quién postulo y quién finalmente aprueba un proyecto de investigación? | El Docente Investigador postula el proyecto; Gestión de Investigación revisa/aprueba | Se postula ante el Gestor de Investigación, quien finalmente lo aprueba. | sin registro | sin registro |
| 25 | fuera de dominio | ¿Cuál es el costo de la pensión mensual de la carrera de Enfermería regular (no por validación)? | No está en el corpus (el catálogo solo da el costo de $2600 del proceso de validación, no de pensiones regulares) | Indica que no tiene esa información y recomienda consultar con Secretaría Académica (rechazo correcto). | N.A. | sin registro |
| 26 | fuera de dominio | ¿Quién es el rector actual del instituto? | No está en el corpus | Indica que no tiene información sobre el rector y recomienda consultar con Secretaría Académica (rechazo correcto). | N.A. | sin registro |
| 27 | fuera de dominio | ¿Cómo cambio la contraseña del WiFi del campus? | No está en el corpus | Indica que no tiene información sobre el WiFi y sugiere consultar con Secretaría Académica (rechazo correcto). | N.A. | sin registro |
| 28 | fuera de dominio | ¿Cuál es el clima en la ciudad hoy? | No está en el corpus / no es competencia del asistente | Indica que no tiene información meteorológica en tiempo real y sugiere consultar con Secretaría Académica (rechazo correcto). | N.A. | sin registro |
| 29 | ambigua | notas | Debería pedir aclaración o dar una respuesta general prudente, no inventar datos | Dice no tener información sobre "notas" ni sobre formatos de vinculación; sugiere consultar con Secretaría Académica. | N.A. | sin registro |
| 30 | ambigua | asdkjaslkdj | Debería indicar que no entiende la pregunta, no inventar una respuesta | Indica que no hay contexto relacionado y que no puede responder; sugiere consultar con Secretaría Académica. | N.A. | sin registro |

¹ La sección 8 describe la respuesta 7 como "respuesta incorrecta pero presentada con confianza" dentro del análisis de fidelidad, pero no le asigna una marca de fidelidad explícita.
² En la corrida 1 (18/08) esta misma respuesta ("Cambiar contraseña") se marcó como no fiel. Para la corrida 2 el documento solo dice que la pregunta 15 "falla en ambas corridas", sin marca de fidelidad propia.

## Totales

| Métrica | Valor de la tesis | Valor en el repositorio | ¿Coincide? | Cómo se verificó |
|---|---|---|---|---|
| Precisión semántica | 14/24 (58,3 %) | 14/24 (58,3 %) | Sí | Total registrado en `justificacion_metricas_tabla_tesis.md` §8. No se puede recalcular pregunta por pregunta. |
| Fidelidad a la fuente | 26/30 (86,7 %) | 26/30 (86,7 %) | Sí | Igual que el anterior: solo existe el total. |
| Fuera de dominio | 4/4 (100 %) | 4/4 (100 %) | Sí | Registrado en §8 y comprobado en el JSON: las respuestas 25–28 son rechazos. |
| Latencia media | 8,85 s | 8,851 s | Sí | Recalculado desde el JSON: media de `tiempo_segundos` sobre las 30 consultas. |

Comprobaciones adicionales sobre el JSON: 30 consultas, 0 errores de ejecución, 22 de dominio + 2 combinadas = 24 (denominador de precisión), 4 fuera de dominio, 2 ambiguas.

## Qué marcas faltan registrar

- **Precisión (10 incorrectas de 24).** El documento identifica 7: las preguntas 7, 9, 10, 13, 15, 20 y 22. Las otras **3 incorrectas no están identificadas** en ningún archivo.
- **Fidelidad (4 no fieles de 30).** Solo la pregunta 22 está calificada de forma expresa como fabricación. Las otras 3 no están identificadas con una marca explícita (ver notas ¹ y ²).
- Las respuestas que, por su contenido, son candidatas a completar esas marcas son la 3 (rechazo de un dato que sí está en el corpus), la 6 (omite el carnet COVID-19), la 11 (añade una acción no esperada) y la 24 (confunde quién postula). Esto es una observación sobre el texto de las respuestas, **no un scoring registrado**: quien hizo la evaluación debe confirmar cuáles son.
