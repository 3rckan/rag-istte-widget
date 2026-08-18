# scripts/evaluate.py
# Sprint 4 (US-04): evaluacion del asistente con un set de consultas.
#
# Corre cada pregunta contra el pipeline RAG (retrieval + generacion) y guarda
# la respuesta, las fuentes recuperadas y el tiempo de respuesta en un reporte
# JSON + Markdown dentro de docs/evaluacion/.
#
# IMPORTANTE: mientras no se reemplacen los PDFs de ejemplo en
# data/reglamentos/ por los documentos oficiales del ISTTE, estos resultados
# solo validan que el PIPELINE funciona (retrieval correcto, latencia,
# comportamiento ante preguntas fuera de alcance). No son evaluacion de
# precision academica real todavia.

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from rag_chain import responder_pregunta

PREGUNTAS = [
    # --- Asistencia (Art. 1) ---
    {"id": 1, "categoria": "asistencia", "pregunta": "¿Cuál es el porcentaje mínimo de asistencia que debo cumplir?"},
    {"id": 2, "categoria": "asistencia", "pregunta": "¿Qué pasa si no cumplo con la asistencia mínima?"},
    {"id": 3, "categoria": "asistencia", "pregunta": "¿En cuánto tiempo puedo justificar una inasistencia por salud?"},
    {"id": 4, "categoria": "asistencia", "pregunta": "¿Ante quién se justifican las inasistencias?"},

    # --- Calificaciones (Art. 2) ---
    {"id": 5, "categoria": "calificaciones", "pregunta": "¿Cuál es la escala de calificaciones del instituto?"},
    {"id": 6, "categoria": "calificaciones", "pregunta": "¿Cuál es la nota mínima para aprobar una asignatura?"},
    {"id": 7, "categoria": "calificaciones", "pregunta": "Tengo un 6 sobre 10, ¿puedo rendir un examen de recuperación?"},
    {"id": 8, "categoria": "calificaciones", "pregunta": "¿Qué rango de notas da derecho a examen de recuperación?"},

    # --- Matrículas y periodos (Art. 4) ---
    {"id": 9, "categoria": "matriculas", "pregunta": "¿Cuándo es el periodo de matrícula ordinaria?"},
    {"id": 10, "categoria": "matriculas", "pregunta": "¿Qué pasa si me matriculo después del plazo ordinario?"},
    {"id": 11, "categoria": "matriculas", "pregunta": "¿Tiene costo adicional la matrícula extraordinaria?"},

    # --- Validación de conocimientos (Art. 5) ---
    {"id": 12, "categoria": "validacion", "pregunta": "¿Puedo validar una materia si ya tengo experiencia laboral en el área?"},
    {"id": 13, "categoria": "validacion", "pregunta": "¿Ante quién se solicita la validación de conocimientos?"},
    {"id": 14, "categoria": "validacion", "pregunta": "¿Qué documentación necesito para validar una asignatura?"},

    # --- Calendario académico ---
    {"id": 15, "categoria": "calendario", "pregunta": "¿Cuándo inician y terminan las clases del periodo 2026-I?"},
    {"id": 16, "categoria": "calendario", "pregunta": "¿Cuáles son las fechas de matrículas ordinarias?"},
    {"id": 17, "categoria": "calendario", "pregunta": "¿Cuáles son las fechas de matrículas extraordinarias?"},
    {"id": 18, "categoria": "calendario", "pregunta": "¿Cuándo es la semana de exámenes finales?"},
    {"id": 19, "categoria": "calendario", "pregunta": "¿Cuándo son las vacaciones o receso académico?"},
    {"id": 20, "categoria": "calendario", "pregunta": "¿Cuándo son los exámenes de recuperación?"},
    {"id": 21, "categoria": "calendario", "pregunta": "¿Dónde se hacen las matrículas ordinarias?"},

    # --- Preguntas combinadas / razonamiento sobre el contexto ---
    {"id": 22, "categoria": "combinada", "pregunta": "Si pierdo una asignatura por inasistencia, ¿puedo rendir el examen de recuperación de julio?"},
    {"id": 23, "categoria": "combinada", "pregunta": "¿Cuántos días tengo entre el fin de matrículas ordinarias y el inicio de clases?"},

    # --- Fuera de alcance (deben responder que no tienen la info) ---
    {"id": 24, "categoria": "fuera_de_alcance", "pregunta": "¿Cuál es el costo de la pensión mensual?"},
    {"id": 25, "categoria": "fuera_de_alcance", "pregunta": "¿Quién es el rector actual del instituto?"},
    {"id": 26, "categoria": "fuera_de_alcance", "pregunta": "¿Cómo cambio mi contraseña del aula virtual?"},
    {"id": 27, "categoria": "fuera_de_alcance", "pregunta": "¿Cuál es el clima en la ciudad hoy?"},

    # --- Ambiguas / mal formuladas ---
    {"id": 28, "categoria": "ambigua", "pregunta": "notas"},
    {"id": 29, "categoria": "ambigua", "pregunta": "asdkjaslkdj"},
    {"id": 30, "categoria": "ambigua", "pregunta": "cuentame sobre el reglamento"},
]


def correr_evaluacion():
    resultados = []
    print(f"\n🧪 Evaluando {len(PREGUNTAS)} consultas...\n")

    for item in PREGUNTAS:
        inicio = time.perf_counter()
        try:
            salida = responder_pregunta(item["pregunta"])
            error = None
        except Exception as exc:  # noqa: BLE001 - queremos registrar cualquier fallo del pipeline
            salida = {"respuesta": None, "fuentes": []}
            error = str(exc)
        duracion = round(time.perf_counter() - inicio, 2)

        resultado = {
            "id": item["id"],
            "categoria": item["categoria"],
            "pregunta": item["pregunta"],
            "respuesta": salida["respuesta"],
            "fuentes": salida["fuentes"],
            "tiempo_segundos": duracion,
            "error": error,
        }
        resultados.append(resultado)

        estado = "❌" if error else "✅"
        print(f"{estado} [{item['id']:02d}/{len(PREGUNTAS)}] ({duracion}s) {item['pregunta']}")

    return resultados


def guardar_reporte(resultados):
    out_dir = Path(__file__).resolve().parent.parent / "docs" / "evaluacion"
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = out_dir / f"resultados_{timestamp}.json"
    json_path.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")

    errores = sum(1 for r in resultados if r["error"])
    sin_fuentes = sum(1 for r in resultados if not r["fuentes"])
    tiempo_prom = round(sum(r["tiempo_segundos"] for r in resultados) / len(resultados), 2)

    md_lines = [
        "# Reporte de evaluacion - Sprint 4",
        "",
        f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "> **Nota:** corrido contra los PDFs de EJEMPLO en `data/reglamentos/` "
        "(no son los documentos oficiales del ISTTE). Sirve para validar el "
        "pipeline (retrieval, latencia, manejo de preguntas fuera de alcance); "
        "hay que volver a correr `python scripts/evaluate.py` una vez se "
        "reemplacen por los PDFs reales.",
        "",
        "## Resumen",
        "",
        f"- Consultas evaluadas: {len(resultados)}",
        f"- Errores del pipeline: {errores}",
        f"- Respuestas sin fuentes recuperadas: {sin_fuentes}",
        f"- Tiempo de respuesta promedio: {tiempo_prom}s",
        "",
        "## Detalle",
        "",
        "| ID | Categoria | Pregunta | Tiempo (s) | Fuentes | Respuesta |",
        "|----|-----------|----------|-----------|---------|-----------|",
    ]
    for r in resultados:
        fuentes = ", ".join(sorted({Path(f["archivo"]).name for f in r["fuentes"]})) or "—"
        respuesta = (r["respuesta"] or f"ERROR: {r['error']}").replace("\n", " ").replace("|", "/")
        if len(respuesta) > 140:
            respuesta = respuesta[:140] + "…"
        md_lines.append(
            f"| {r['id']} | {r['categoria']} | {r['pregunta']} | {r['tiempo_segundos']} | {fuentes} | {respuesta} |"
        )

    md_path = out_dir / f"resultados_{timestamp}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\n📄 Reporte guardado en:\n  {json_path}\n  {md_path}")
    print(f"\n📊 Resumen: {len(resultados)} consultas, {errores} errores, "
          f"{sin_fuentes} sin fuentes, {tiempo_prom}s promedio")


if __name__ == "__main__":
    resultados = correr_evaluacion()
    guardar_reporte(resultados)
