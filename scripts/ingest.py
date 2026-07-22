# scripts/ingest.py
# Sprint 2 (US-02, US-03): script de ingesta de datos mejorado
# Objetivo: leer los PDFs con contexto de imágenes y guardarlos como vectores en ChromaDB

import glob
import os
import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

DATA_DIR = "data/reglamentos"
PERSIST_DIR = "chroma_db"

# Descripciones de imágenes importantes por documento y página
# Esto proporciona contexto visual que la extracción de PDF no puede captar
IMAGE_CONTEXT = {
    "guía_del_docente_eva_periodo_p37.pdf": {
        2: "Interfaz web de acceso a Tu Aula Virtual ISTTE con sitio oficial y botón verde de acceso",
        3: "Estructura del aula: Cabecera con información de asignatura, Generalidades con normas y chat, Bloques de Aprendizaje",
        4: "Bloques educativos: Biblioteca Académica con videos, Unidades de Estudio, Actividades en parciales, Evaluaciones",
        5: "Sistema de evaluación con rueda interactiva de valores - Aprendizaje Basado en Problemas",
        6: "Bloque de Tutorías (foro para solicitar tutoría) y Portafolio del Estudiante para evidencias",
    },
    "guía_del_estudiante_eva_periodo_p37.pdf": {
        2: "Pantalla de acceso a Tu Aula Virtual con botón verde y mensaje de autenticación",
        3: "Estructura: Cabecera, Generalidades con normas/silabo, Bloques de Aprendizaje",
        4: "Unidades de Estudio con Biblioteca Académica, Materiales de apoyo, Actividades en parciales",
        5: "Evaluaciones por unidades y dos exámenes, Sistema ABP con actividades interactivas",
        6: "Tutorías (solicitar por foro) y Portafolio (recolectar evidencias de aprendizaje)",
        7: "Procedimiento de 7 pasos para cargar actividades: click, agregar, seleccionar, guardar",
    },
}


def cargar_documentos():
    """Lee todos los PDFs de DATA_DIR y devuelve una lista de documentos enriquecidos."""
    documentos = []
    rutas_pdf = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    
    print(f"📂 Encontrados {len(rutas_pdf)} archivos PDF")
    
    for ruta in rutas_pdf:
        print(f"  📄 Procesando: {Path(ruta).name}")
        loader = PyPDFLoader(ruta)
        docs = loader.load()
        
        # Enriquecer documentos con contexto de imágenes
        pdf_name = Path(ruta).name
        for doc in docs:
            page_num = doc.metadata.get("page", 0)
            
            # Agregar contexto de imagen si existe
            if pdf_name in IMAGE_CONTEXT and page_num in IMAGE_CONTEXT[pdf_name]:
                img_context = IMAGE_CONTEXT[pdf_name][page_num]
                doc.page_content += f"\n\n[CONTEXTO VISUAL]: {img_context}"
        
        documentos.extend(docs)
    
    return documentos


def dividir_en_chunks(documentos):
    """Divide los documentos en fragmentos manejables para el embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700, 
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documentos)
    print(f"✂️  Divididos en {len(chunks)} chunks")
    return chunks


def guardar_en_chroma(chunks):
    """Convierte los chunks en vectores y los persiste en ChromaDB."""
    print(f"🔄 Generando embeddings con Ollama (nomic-embed-text)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    print(f"💾 Guardando en ChromaDB ({PERSIST_DIR})...")
    Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    print(f"✅ Base de datos creada exitosamente")


if __name__ == "__main__":
    print("\n🚀 Iniciando ingesta de documentos...\n")
    
    # Cargar
    docs = cargar_documentos()
    if not docs:
        print("⚠️  No se encontraron documentos. Verifica que existan PDFs en data/reglamentos/")
        sys.exit(1)
    
    print(f"✓ Cargados {len(docs)} documentos\n")
    
    # Dividir
    chunks = dividir_en_chunks(docs)
    
    # Guardar
    print()
    guardar_en_chroma(chunks)
    
    print(f"\n✅ Ingesta completa: {len(chunks)} fragmentos guardados")
