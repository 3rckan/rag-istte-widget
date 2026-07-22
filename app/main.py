# app/main.py
# API del asistente virtual RAG. Expone el endpoint /query que usa el
# widget de chat para hacerle preguntas al instituto.

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag_chain import responder_pregunta

app = FastAPI(title="Asistente Virtual RAG - ISTTE")

# En desarrollo se permite cualquier origen para poder probar el widget
# como archivo HTML local. En produccion (Sprint 4) esto debe restringirse
# al dominio real de la web del instituto.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/widget", StaticFiles(directory=str(static_dir), html=True), name="widget")


class PreguntaRequest(BaseModel):
    pregunta: str


@app.post("/query")
def query(request: PreguntaRequest):
    return responder_pregunta(request.pregunta)
