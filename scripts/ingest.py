# scripts/ingest.py
# Sprint 2 (US-02, US-03): script de ingesta de datos.
# Objetivo: leer los PDFs de data/reglamentos/, dividirlos en fragmentos (chunks)
# y guardarlos como vectores en ChromaDB para poder buscarlos semánticamente después.

import glob
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

DATA_DIR = "data/reglamentos"
PERSIST_DIR = "chroma_db"


def cargar_documentos():
    """Lee todos los PDFs de DATA_DIR y devuelve una lista de documentos."""
    documentos = []
    rutas_pdf = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    for ruta in rutas_pdf:
        loader = PyPDFLoader(ruta)
        documentos.extend(loader.load())
    return documentos


def dividir_en_chunks(documentos):
    """Divide los documentos en fragmentos manejables para el embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    return splitter.split_documents(documentos)


def guardar_en_chroma(chunks):
    """Convierte los chunks en vectores y los persiste en ChromaDB."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)


if __name__ == "__main__":
    docs = cargar_documentos()
    chunks = dividir_en_chunks(docs)
    guardar_en_chroma(chunks)
    print(f"Ingesta completa: {len(chunks)} fragmentos guardados en {PERSIST_DIR}")
