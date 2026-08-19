# scripts/evaluate_oficial.py
# Evaluacion oficial para la memoria de titulacion (Capitulo 5).
#
# Corre un set de 30 preguntas con respuesta esperada conocida (verificada
# manualmente contra el texto de los 3 PDFs institucionales reales en
# data/reglamentos/: ISTTE_Catalogo_Procesos_Digitales.pdf,
# matriz_roles_permisos_depurada.pdf, videos_conocetuplataformaISTTE.pdf)
# contra el pipeline RAG real (retrieval + generacion con Llama 3.2).
#
# Guarda respuesta, fuentes recuperadas y tiempo de respuesta en un JSON.
# El scoring de precision semantica y fidelidad a la fuente se hace en un
# paso aparte (revision manual contra "esperado"), documentado en
# docs/evaluacion/justificacion_metricas_tabla.md

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from rag_chain import responder_pregunta

PREGUNTAS = [
    # --- En dominio: Catalogo de Procesos y Servicios Digitales ---
    {"id": 1, "categoria": "dominio", "pregunta": "¿Cuál es el correo institucional general de contacto del ISTTE?",
     "esperado": "info@istte.edu.ec"},
    {"id": 2, "categoria": "dominio", "pregunta": "¿Cuál es el costo del proceso de validación de conocimientos y experiencia para ingresar a una carrera?",
     "esperado": "$2600, con opción de pago de contado, tarjeta de crédito, u 8 pagos mensuales"},
    {"id": 3, "categoria": "dominio", "pregunta": "¿Cuántos años de edad debe tener un aspirante para el proceso de validación de conocimientos y experiencia?",
     "esperado": "25 años o más"},
    {"id": 4, "categoria": "dominio", "pregunta": "¿Cuál es el enlace del portal de empleo del ISTTE?",
     "esperado": "https://portalempleo.istte.edu.ec/"},
    {"id": 5, "categoria": "dominio", "pregunta": "¿Cuál es el horario de atención de la Sede Matriz (La Magdalena)?",
     "esperado": "Lunes a viernes, 8:00 a 19:00"},
    {"id": 6, "categoria": "dominio", "pregunta": "¿Qué documento relacionado a salud se pide en PDF antes de iniciar las Prácticas Preprofesionales?",
     "esperado": "Carnet de vacunación COVID-19 (y para carreras de Salud y Bienestar, vacunas de hepatitis B y tétanos)"},
    {"id": 7, "categoria": "dominio", "pregunta": "¿Qué módulos están disponibles en el SIACAD tras iniciar sesión?",
     "esperado": "Académico, Investigación, Vinculación, PPP, Reportes y Configuración"},
    {"id": 8, "categoria": "dominio", "pregunta": "¿Qué información muestra el reporte de Notas y Asistencias de un estudiante en SIACAD?",
     "esperado": "Promedio (GPA), créditos aprobados, y detalle de notas y porcentaje de asistencia por materia y nivel, con el docente responsable"},

    # --- En dominio: Matriz de Roles y Permisos ---
    {"id": 9, "categoria": "dominio", "pregunta": "¿Qué rol se encarga de tomar la asistencia diaria y registrar notas parciales de los estudiantes?",
     "esperado": "Docente"},
    {"id": 10, "categoria": "dominio", "pregunta": "¿Quién aprueba la emisión de certificados e informes finales de investigación?",
     "esperado": "Gestión de Investigación"},
    {"id": 11, "categoria": "dominio", "pregunta": "¿Qué acciones puede realizar el Docente Director de Proyecto en Vinculación con la Sociedad?",
     "esperado": "Postular proyectos, inscribir estudiantes, supervisar el seguimiento en campo y aprobar el cumplimiento de horas"},
    {"id": 12, "categoria": "dominio", "pregunta": "¿Quién administra el uso de talleres, laboratorios y equipos informáticos, y reporta incidencias técnicas?",
     "esperado": "Técnico de Laboratorio"},
    {"id": 13, "categoria": "dominio", "pregunta": "¿Qué rol brinda seguimiento a estudiantes con Necesidades Educativas Especiales (NEE)?",
     "esperado": "Docente y Bienestar Estudiantil (UBE)"},

    # --- En dominio: tutoriales de plataformas (EVA, SIACAD, correo, biblioteca) ---
    {"id": 14, "categoria": "dominio", "pregunta": "¿Cuáles son los campos obligatorios para cambiar la contraseña en la plataforma EVA?",
     "esperado": "Contraseña actual, nueva contraseña y confirmar nueva contraseña"},
    {"id": 15, "categoria": "dominio", "pregunta": "¿Cuál es el nombre del botón para guardar los cambios al cambiar la contraseña en EVA?",
     "esperado": "\"Guardar cambios\""},
    {"id": 16, "categoria": "dominio", "pregunta": "¿Qué formato de archivo se recomienda usar al enviar una tarea en la plataforma EVA?",
     "esperado": "PDF"},
    {"id": 17, "categoria": "dominio", "pregunta": "¿Cuál es el tamaño máximo permitido para adjuntar un archivo al enviar un correo institucional?",
     "esperado": "50 MB"},
    {"id": 18, "categoria": "dominio", "pregunta": "¿Qué plataforma externa se usa para la biblioteca virtual del instituto?",
     "esperado": "eLibro (elibro.net)"},
    {"id": 19, "categoria": "dominio", "pregunta": "¿Cuál es la regla para formar la contraseña inicial de acceso a la biblioteca virtual eLibro?",
     "esperado": "Número de cédula del estudiante + primera letra del nombre en minúscula"},
    {"id": 20, "categoria": "dominio", "pregunta": "¿Qué se usa como nombre de usuario para iniciar sesión en el SIACAD?",
     "esperado": "El número de cédula del estudiante"},
    {"id": 21, "categoria": "dominio", "pregunta": "¿Qué opciones aparecen dentro del menú 'Búsquedas' del SIACAD?",
     "esperado": "Buscar evaluación al docente, y Buscar Matrículas"},
    {"id": 22, "categoria": "dominio", "pregunta": "¿Cuál es el dominio de correo institucional que usan los estudiantes del Tecnoecuatoriano?",
     "esperado": "@tecnovirtual.edu.ec"},

    # --- Combinadas / razonamiento sobre el contexto ---
    {"id": 23, "categoria": "combinada", "pregunta": "Si quiero saber mis notas y mi porcentaje de asistencia, ¿en qué sistema y en qué reporte lo encuentro?",
     "esperado": "En el SIACAD, en el reporte de Notas y Asistencias (Reportes > Notas y Asistencias Alumnos)"},
    {"id": 24, "categoria": "combinada", "pregunta": "Como estudiante, ¿ante quién postulo y quién finalmente aprueba un proyecto de investigación?",
     "esperado": "El Docente Investigador postula el proyecto; Gestión de Investigación revisa/aprueba"},

    # --- Fuera de dominio (el corpus NO tiene esta información) ---
    {"id": 25, "categoria": "fuera_de_dominio", "pregunta": "¿Cuál es el costo de la pensión mensual de la carrera de Enfermería regular (no por validación)?",
     "esperado": "No está en el corpus (el catálogo solo da el costo de $2600 del proceso de validación, no de pensiones regulares)"},
    {"id": 26, "categoria": "fuera_de_dominio", "pregunta": "¿Quién es el rector actual del instituto?",
     "esperado": "No está en el corpus"},
    {"id": 27, "categoria": "fuera_de_dominio", "pregunta": "¿Cómo cambio la contraseña del WiFi del campus?",
     "esperado": "No está en el corpus"},
    {"id": 28, "categoria": "fuera_de_dominio", "pregunta": "¿Cuál es el clima en la ciudad hoy?",
     "esperado": "No está en el corpus / no es competencia del asistente"},

    # --- Ambiguas / mal formuladas ---
    {"id": 29, "categoria": "ambigua", "pregunta": "notas", "esperado": "Debería pedir aclaración o dar una respuesta general prudente, no inventar datos"},
    {"id": 30, "categoria": "ambigua", "pregunta": "asdkjaslkdj", "esperado": "Debería indicar que no entiende la pregunta, no inventar una respuesta"},
]


def correr_evaluacion():
    resultados = []
    print(f"\nEvaluando {len(PREGUNTAS)} consultas...\n")

    for item in PREGUNTAS:
        inicio = time.perf_counter()
        try:
            salida = responder_pregunta(item["pregunta"])
            error = None
        except Exception as exc:  # noqa: BLE001
            salida = {"respuesta": None, "fuentes": []}
            error = str(exc)
        duracion = round(time.perf_counter() - inicio, 2)

        resultado = {
            "id": item["id"],
            "categoria": item["categoria"],
            "pregunta": item["pregunta"],
            "esperado": item["esperado"],
            "respuesta": salida["respuesta"],
            "fuentes": [f["archivo"] for f in salida["fuentes"]],
            "tiempo_segundos": duracion,
            "error": error,
        }
        resultados.append(resultado)

        estado = "ERROR" if error else "OK"
        print(f"[{estado}] [{item['id']:02d}/{len(PREGUNTAS)}] ({duracion}s) {item['pregunta']}")

    return resultados


def guardar_reporte(resultados):
    out_dir = Path(__file__).resolve().parent.parent / "docs" / "evaluacion"
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = out_dir / f"resultados_oficiales_{timestamp}.json"
    json_path.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")

    tiempo_prom = round(sum(r["tiempo_segundos"] for r in resultados) / len(resultados), 2)
    print(f"\nReporte guardado en: {json_path}")
    print(f"Tiempo de respuesta promedio (crudo, sin scoring): {tiempo_prom}s")
    return json_path


if __name__ == "__main__":
    resultados = correr_evaluacion()
    guardar_reporte(resultados)
