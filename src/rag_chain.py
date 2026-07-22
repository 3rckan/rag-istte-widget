# src/rag_chain.py
# Logica central del RAG: dada una pregunta del estudiante, busca contexto
# relevante en ChromaDB (retrieval) y se lo pasa a Llama 3.2 para que
# genere la respuesta (generation).

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

PERSIST_DIR = "chroma_db"

PROMPT_TEMPLATE = """Eres un asistente virtual del Instituto Superior Tecnologico Tecnoecuatoriano (ISTTE).
Responde la pregunta del estudiante usando UNICAMENTE la informacion del siguiente contexto.
Si el contexto no contiene la respuesta, di claramente que no tienes esa informacion y
sugiere consultar con secretaria academica. Responde en espanol, de forma breve y clara.

Contexto:
{contexto}

Pregunta del estudiante:
{pregunta}

Respuesta:"""


def _obtener_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


def responder_pregunta(pregunta: str, k: int = 4) -> dict:
    """Busca los k chunks mas relevantes para la pregunta y genera una respuesta con Llama 3.2."""
    vectorstore = _obtener_vectorstore()
    documentos = vectorstore.similarity_search(pregunta, k=k)

    contexto = "\n\n".join(doc.page_content for doc in documentos)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    modelo = OllamaLLM(model="llama3.2")
    cadena = prompt | modelo

    respuesta = cadena.invoke({"contexto": contexto, "pregunta": pregunta})

    fuentes = [
        {
            "archivo": doc.metadata.get("source", "desconocido"),
            "pagina": doc.metadata.get("page", None),
        }
        for doc in documentos
    ]
    return {"respuesta": respuesta, "fuentes": fuentes}
