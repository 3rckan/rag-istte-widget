#!/usr/bin/env python3
"""
Script para procesar PDFs extrayendo texto e información de imágenes.
Combina el contexto textual con descripciones de elementos visuales importantes.
"""

import os
import sys
from pathlib import Path
from pypdf import PdfReader
import fitz  # PyMuPDF para extraer imágenes

# Agregar src al path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

DATA_DIR = "data/reglamentos"

# Descripciones de imágenes importantes por documento y página
IMAGE_DESCRIPTIONS = {
    "guía_del_docente_eva_periodo_p37.pdf": {
        "page_2": {
            "descripcion": "Interfaz de acceso a Tu Aula Virtual ISTTE - Sitio web oficial con botón verde de acceso",
            "ubicacion": "Sección: Acceso a Tu Aula Virtual ISTTE"
        },
        "page_3": {
            "descripcion": "Estructura del aula virtual: Cabecera (información de asignatura), Generalidades (normas y chat), Bloques de Aprendizaje (unidades, actividades, evaluaciones)",
            "ubicacion": "Sección: Estructura de cursos"
        },
        "page_4": {
            "descripcion": "Bloques de aprendizaje detallados: Biblioteca Académica con videos, Unidades de Estudio, Actividades en parciales, Evaluaciones",
            "ubicacion": "Sección: Componentes del Aula"
        },
        "page_5": {
            "descripcion": "Sistema de evaluación y Aprendizaje Basado en Problemas (ABP) con rueda de valores interactiva",
            "ubicacion": "Sección: Evaluaciones y ABP"
        },
        "page_6": {
            "descripcion": "Bloque de Tutorías con foro de solicitud y Portafolio del Estudiante para recopilar evidencias",
            "ubicacion": "Sección: Tutorías y Portafolio"
        }
    },
    "guía_del_estudiante_eva_periodo_p37.pdf": {
        "page_2": {
            "descripcion": "Pantalla de acceso a Tu Aula Virtual ISTTE con ubicación del botón verde y mensaje de error de autenticación",
            "ubicacion": "Sección: Acceso"
        },
        "page_3": {
            "descripcion": "Estructura general: Cabecera (información), Generalidades (normas/silabo), Bloques de Aprendizaje (recursos educativos)",
            "ubicacion": "Sección: Componentes principales"
        },
        "page_4": {
            "descripcion": "Componentes educativos: Unidades de Estudio con biblioteca académica y materiales de apoyo, Actividades en dos parciales",
            "ubicacion": "Sección: Materiales y Actividades"
        },
        "page_5": {
            "descripcion": "Evaluaciones disponibles por unidades y dos exámenes, Sistema de Aprendizaje Basado en Problemas con actividades interactivas",
            "ubicacion": "Sección: Sistema Evaluativo"
        },
        "page_6": {
            "descripcion": "Bloque de Tutorías: Usar foro para solicitar tutoría al profesor; Portafolio: recolectar evidencias de aprendizaje",
            "ubicacion": "Sección: Tutorías y Portafolio"
        },
        "page_7": {
            "descripcion": "Proceso para cargar actividades: 7 pasos ilustrados (clic en etiqueta, agregar entrega, seleccionar archivo, guardar cambios)",
            "ubicacion": "Sección: Procedimiento técnico"
        }
    }
}


def extract_text_from_pdf(pdf_path):
    """Extrae texto completo del PDF."""
    try:
        reader = PdfReader(pdf_path)
        text_by_page = {}
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            text_by_page[f"page_{page_num}"] = text
            
        return text_by_page
    except Exception as e:
        print(f"Error extrayendo texto de {pdf_path}: {e}")
        return {}


def combine_text_with_image_context(pdf_name, text_by_page):
    """Combina texto extraído con descripciones de imágenes importantes."""
    
    descriptions = IMAGE_DESCRIPTIONS.get(pdf_name.lower(), {})
    combined_content = {}
    
    for page_key, text in text_by_page.items():
        content = text
        
        # Agregar descripción de imagen si existe
        if page_key in descriptions:
            img_info = descriptions[page_key]
            content += f"\n\n[ELEMENTO VISUAL IMPORTANTE]\n"
            content += f"Ubicación: {img_info['ubicacion']}\n"
            content += f"Descripción: {img_info['descripcion']}\n"
        
        combined_content[page_key] = content
    
    return combined_content


def create_enriched_documents(pdf_path, pdf_name):
    """Crea documentos enriquecidos con contexto de imágenes."""
    
    print(f"\n📄 Procesando: {pdf_name}")
    
    # Extraer texto
    text_by_page = extract_text_from_pdf(pdf_path)
    if not text_by_page:
        print(f"⚠️  No se pudo extraer texto de {pdf_name}")
        return []
    
    # Combinar con descripciones de imágenes
    enriched_pages = combine_text_with_image_context(pdf_name, text_by_page)
    
    # Crear documentos para ChromaDB
    documents = []
    for page_key, content in enriched_pages.items():
        if content.strip():  # Solo si hay contenido
            page_num = page_key.replace("page_", "")
            doc = {
                "content": content,
                "metadata": {
                    "source": str(pdf_path),
                    "page": int(page_num),
                    "pdf_name": pdf_name,
                    "type": "documento_educativo"
                }
            }
            documents.append(doc)
    
    print(f"✓ Extraídas {len(documents)} páginas de {pdf_name}")
    return documents


def process_all_pdfs():
    """Procesa todos los PDFs en la carpeta de reglamentos."""
    
    all_documents = []
    pdf_files = list(Path(DATA_DIR).glob("*.pdf"))
    
    print(f"\n🔍 Encontrados {len(pdf_files)} archivos PDF")
    
    for pdf_path in pdf_files:
        docs = create_enriched_documents(str(pdf_path), pdf_path.name)
        all_documents.extend(docs)
    
    return all_documents


if __name__ == "__main__":
    documents = process_all_pdfs()
    
    print(f"\n✅ Total de documentos procesados: {len(documents)}")
    print("\nEjemplo de primer documento:")
    if documents:
        print(f"Fuente: {documents[0]['metadata']['source']}")
        print(f"Página: {documents[0]['metadata']['page']}")
        print(f"Contenido (primeros 200 caracteres):")
        print(documents[0]['content'][:200] + "...")
