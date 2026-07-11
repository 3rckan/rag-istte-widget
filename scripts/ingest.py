# scripts/ingest.py
# Sprint 2 (US-02, US-03): script de ingesta de datos.
# Objetivo: leer los PDFs de data/reglamentos/, dividirlos en fragmentos (chunks)
# y guardarlos como vectores en ChromaDB para poder buscarlos semánticamente después.
#
# Esto es un ESQUELETO para cuando empieces el Sprint 2 — no lo llenes todavía,
# primero completa el entorno del Sprint 1 (Ollama instalado + PDFs recopilados).

# TODO (Sprint 2): importar PyPDFLoader de langchain_community.document_loaders
# TODO (Sprint 2): importar RecursiveCharacterTextSplitter de langchain.text_splitter
# TODO (Sprint 2): importar Chroma de langchain_community.vectorstores
# TODO (Sprint 2): importar OllamaEmbeddings de langchain_ollama

DATA_DIR = "data/reglamentos"
PERSIST_DIR = "chroma_db"


def cargar_documentos():
    """Lee todos los PDFs de DATA_DIR y devuelve una lista de documentos."""
    # TODO: recorrer DATA_DIR, cargar cada PDF con PyPDFLoader
    raise NotImplementedError


def dividir_en_chunks(documentos):
    """Divide los documentos en fragmentos manejables para el embedding."""
    # TODO: usar RecursiveCharacterTextSplitter (chunk_size ~500-800, overlap ~100)
    raise NotImplementedError


def guardar_en_chroma(chunks):
    """Convierte los chunks en vectores y los persiste en ChromaDB."""
    # TODO: crear OllamaEmbeddings(model="nomic-embed-text")
    # TODO: Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    raise NotImplementedError


if __name__ == "__main__":
    docs = cargar_documentos()
    chunks = dividir_en_chunks(docs)
    guardar_en_chroma(chunks)
    print(f"Ingesta completa: {len(chunks)} fragmentos guardados en {PERSIST_DIR}")
