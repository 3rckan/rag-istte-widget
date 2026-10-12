# Anexo 4. Fragmentos de código del sistema ISTTE-Bot

Fragmentos copiados textualmente del repositorio local (rama `master`, commit `5a6f083`,
árbol de trabajo limpio). No se editó ninguna línea; los números de línea corresponden al archivo original.

## a.1) Templates del prompt

**`src/rag_chain.py`** (líneas 32–63)

```python
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
```

## a.2) `_es_saludo_o_charla`

**`src/rag_chain.py`** (líneas 81–89)

```python
def _es_saludo_o_charla(pregunta: str) -> bool:
    """Detecta saludos/charla casual por palabras clave, sin usar el LLM para decidir.

    No se delega esta decision al modelo porque no es determinista: la misma
    pregunta ("hola") a veces se respondia bien y a veces se rechazaba con
    "no tengo informacion" (ver docs/evaluacion/diagnostico_falsos_negativos_20260814.md).
    """
    texto = _normalizar(pregunta)
    return any(re.match(patron, texto) for patron in PATRONES_SALUDO)
```

## a.3) `responder_pregunta`

**`src/rag_chain.py`** (líneas 97–121)

```python
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
```

## b) `dividir_en_chunks`

**`scripts/ingest.py`** (líneas 67–76)

```python
def dividir_en_chunks(documentos):
    """Divide los documentos en fragmentos manejables para el embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documentos)
    print(f"✂️  Divididos en {len(chunks)} chunks")
    return chunks
```
