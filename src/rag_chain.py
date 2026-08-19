# src/rag_chain.py
# Logica central del RAG: dada una pregunta del estudiante, busca contexto
# relevante en ChromaDB (retrieval) y se lo pasa a Llama 3.2 para que
# genere la respuesta (generation).

import os
import re

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

PERSIST_DIR = "chroma_db"

# En desarrollo, Ollama corre en localhost. En despliegue (Sprint 4) puede
# vivir en otro host/contenedor: se configura con la variable de entorno
# OLLAMA_BASE_URL (ver docs/DEPLOY_RENDER.md).
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Instrucciones (rol "system") separadas del mensaje del estudiante (rol
# "human"). Antes iban en un solo bloque de texto sin distincion de roles;
# esta separacion le da al prompt un limite mas claro entre "instrucciones
# del asistente" y "lo que escribio el estudiante" (hallazgo de seguridad
# del /cso: superficie de prompt injection). Nota: OllamaLLM usa el endpoint
# de completado de Ollama, que aplana estos roles a texto ("System: ...\n
# Human: ..."), no son mensajes separados a nivel de API como en un chat
# real — es una mejora de estructura, no una barrera de seguridad dura.
SISTEMA_TEMPLATE = """Eres un asistente virtual del Instituto Superior Tecnologico Tecnoecuatoriano (ISTTE).
Responde la pregunta del estudiante usando UNICAMENTE la informacion del contexto que te
llega en el siguiente mensaje. Si el contexto menciona el tema de la pregunta, aunque sea
de forma parcial o indirecta, usa esa informacion para responder. Solo si el contexto no
menciona el tema en absoluto, di claramente que no tienes esa informacion y sugiere
consultar con secretaria academica. Responde en espanol, de forma breve y clara."""

HUMANO_TEMPLATE = """Contexto:
{contexto}

Pregunta del estudiante:
{pregunta}"""

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SISTEMA_TEMPLATE),
    HumanMessagePromptTemplate.from_template(HUMANO_TEMPLATE),
])

# Prompt separado para saludos/charla casual: sin contexto de PDFs de por medio,
# para que el modelo no tenga que "elegir" entre dos instrucciones a la vez.
SALUDO_SISTEMA_TEMPLATE = """Eres un asistente virtual del Instituto Superior Tecnologico Tecnoecuatoriano (ISTTE).
El estudiante te escribio un saludo o un mensaje de charla casual, no una pregunta sobre
el instituto. Respondele de forma breve, natural y amigable en espanol, invitandolo a
preguntar sobre reglamentos, calendarios o tramites academicos."""

SALUDO_HUMANO_TEMPLATE = """Mensaje del estudiante:
{pregunta}"""

SALUDO_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SALUDO_SISTEMA_TEMPLATE),
    HumanMessagePromptTemplate.from_template(SALUDO_HUMANO_TEMPLATE),
])

# Frases comunes de saludo/charla casual al inicio del mensaje (sin tildes, en minuscula).
PATRONES_SALUDO = [
    r"^hola\b", r"^buenas\b", r"^buenos dias\b", r"^buenas tardes\b", r"^buenas noches\b",
    r"^hey\b", r"^que tal\b", r"^como estas\b", r"^gracias\b", r"^muchas gracias\b",
    r"^adios\b", r"^chao\b", r"^hasta luego\b", r"^quien eres\b", r"^que eres\b",
    r"^que puedes hacer\b", r"^en que me puedes ayudar\b", r"^ayuda\b",
]


def _normalizar(texto: str) -> str:
    """Minuscula y sin tildes, para comparar contra PATRONES_SALUDO sin depender de acentos."""
    texto = texto.strip().lower()
    reemplazos = str.maketrans("áéíóúñ", "aeioun")
    return texto.translate(reemplazos)


def _es_saludo_o_charla(pregunta: str) -> bool:
    """Detecta saludos/charla casual por palabras clave, sin usar el LLM para decidir.

    No se delega esta decision al modelo porque no es determinista: la misma
    pregunta ("hola") a veces se respondia bien y a veces se rechazaba con
    "no tengo informacion" (ver docs/evaluacion/diagnostico_falsos_negativos_20260814.md).
    """
    texto = _normalizar(pregunta)
    return any(re.match(patron, texto) for patron in PATRONES_SALUDO)


def _obtener_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


def responder_pregunta(pregunta: str, k: int = 8) -> dict:
    """Si es saludo/charla casual, responde sin retrieval. Si no, busca los k chunks
    mas relevantes en ChromaDB y genera la respuesta con Llama 3.2 usando solo ese contexto."""
    modelo = OllamaLLM(model="llama3.2", base_url=OLLAMA_BASE_URL)

    if _es_saludo_o_charla(pregunta):
        respuesta = (SALUDO_PROMPT_TEMPLATE | modelo).invoke({"pregunta": pregunta})
        return {"respuesta": respuesta, "fuentes": []}

    vectorstore = _obtener_vectorstore()
    documentos = vectorstore.similarity_search(pregunta, k=k)

    contexto = "\n\n".join(doc.page_content for doc in documentos)
    cadena = PROMPT_TEMPLATE | modelo

    respuesta = cadena.invoke({"contexto": contexto, "pregunta": pregunta})

    fuentes = [
        {
            "archivo": doc.metadata.get("source", "desconocido"),
            "pagina": doc.metadata.get("page", None),
        }
        for doc in documentos
    ]
    return {"respuesta": respuesta, "fuentes": fuentes}
