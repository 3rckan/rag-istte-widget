#!/usr/bin/env python3
"""
Script helper para gestionar PDFs - verificar, copiar, validar archivos
"""

import os
import shutil
from pathlib import Path

DATA_DIR = "data/reglamentos"

REQUIRED_PDFS = {
    "guía_del_docente_eva_periodo_p37.pdf": "Guía para docentes del aula virtual ISTTE",
    "guía_del_estudiante_eva_periodo_p37.pdf": "Guía para estudiantes del aula virtual ISTTE",
}

EXAMPLE_PDFS = {
    "calendario_academico_ejemplo.pdf": "Calendario académico de ejemplo",
    "reglamento_academico_ejemplo.pdf": "Reglamento académico de ejemplo",
}


def verificar_pdfs():
    """Verifica qué PDFs existen en la carpeta de reglamentos."""
    print("\n📂 Verificación de archivos PDF\n")
    print(f"Carpeta: {Path(DATA_DIR).absolute()}\n")
    
    # Archivos requeridos
    print("📌 PDFs REQUERIDOS (nuevos):")
    for pdf_name, descripcion in REQUIRED_PDFS.items():
        ruta = Path(DATA_DIR) / pdf_name
        estado = "✅" if ruta.exists() else "❌"
        print(f"  {estado} {pdf_name}")
        print(f"     {descripcion}")
        if ruta.exists():
            size_mb = ruta.stat().st_size / (1024 * 1024)
            print(f"     Tamaño: {size_mb:.2f} MB")
    
    # Archivos de ejemplo
    print("\n📝 PDFs DE EJEMPLO:")
    for pdf_name, descripcion in EXAMPLE_PDFS.items():
        ruta = Path(DATA_DIR) / pdf_name
        estado = "✅" if ruta.exists() else "❌"
        print(f"  {estado} {pdf_name}")
        print(f"     {descripcion}")
        if ruta.exists():
            size_mb = ruta.stat().st_size / (1024 * 1024)
            print(f"     Tamaño: {size_mb:.2f} MB")
    
    # Verificar total
    archivos = list(Path(DATA_DIR).glob("*.pdf"))
    print(f"\n📊 Total de PDFs encontrados: {len(archivos)}/{len(REQUIRED_PDFS) + len(EXAMPLE_PDFS)}")
    
    return len(archivos)


def listar_contenido():
    """Lista el contenido actual de la carpeta de reglamentos."""
    print("\n📋 Contenido de la carpeta:\n")
    
    if not Path(DATA_DIR).exists():
        print(f"  ⚠️  La carpeta {DATA_DIR} no existe")
        return
    
    archivos = list(Path(DATA_DIR).iterdir())
    if not archivos:
        print(f"  (carpeta vacía)")
        return
    
    for archivo in sorted(archivos):
        if archivo.is_file():
            size_kb = archivo.stat().st_size / 1024
            print(f"  {archivo.name} ({size_kb:.1f} KB)")


def instrucciones():
    """Muestra instrucciones detalladas."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   INSTRUCCIONES DE INSTALACIÓN DE PDFs                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

PASO 1: Coloca los archivos PDF
──────────────────────────────────
Los dos nuevos PDFs deben guardarse en:
  
  c:\\proyecto_istte\\rag-istte-widget\\data\\reglamentos\\

Con estos nombres exactos:
  
  ✓ guía_del_docente_eva_periodo_p37.pdf
  ✓ guía_del_estudiante_eva_periodo_p37.pdf

PASO 2: Verifica que estén en la carpeta
──────────────────────────────────────────
Ejecuta este script nuevamente:
  
  python scripts/manage_pdfs.py

Deberías ver "✅" al lado de ambos archivos.

PASO 3: Ejecuta la ingesta
──────────────────────────
Una vez copiados, ejecuta:
  
  python scripts/ingest.py

Este proceso:
  1. Lee todos los PDFs
  2. Extrae el texto
  3. Agrega contexto de imágenes
  4. Genera embeddings
  5. Actualiza ChromaDB

PASO 4: Prueba el asistente
───────────────────────────
El servidor se recargará automáticamente. Luego prueba con preguntas como:
  
  - "¿Cómo accedo a Tu Aula Virtual?"
  - "¿Cuáles son los componentes del aula?"
  - "¿Cómo cargo una actividad?"
  - "¿Qué es el Portafolio del Estudiante?"

═════════════════════════════════════════════════════════════════════════════════
    """)


def main():
    """Función principal."""
    import sys
    
    print("\n🔧 Gestor de PDFs del Sistema RAG ISTTE\n")
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        if comando == "check":
            verificar_pdfs()
        elif comando == "list":
            listar_contenido()
        elif comando == "help":
            instrucciones()
        else:
            print(f"Comando desconocido: {comando}")
            print("\nComandos disponibles:")
            print("  check  - Verificar estado de los PDFs")
            print("  list   - Listar archivos en la carpeta")
            print("  help   - Mostrar instrucciones detalladas")
    else:
        # Mostrar estado por defecto
        verificar_pdfs()
        print("\n💡 Comandos disponibles:")
        print("  python scripts/manage_pdfs.py check  - Verificar PDFs")
        print("  python scripts/manage_pdfs.py list   - Listar archivos")
        print("  python scripts/manage_pdfs.py help   - Ver instrucciones")


if __name__ == "__main__":
    main()
