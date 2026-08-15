# app/main.py
# API del asistente virtual RAG. Expone el endpoint /query que usa el
# widget de chat para hacerle preguntas al instituto.

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag_chain import responder_pregunta

load_dotenv()

app = FastAPI(title="Asistente Virtual RAG - ISTTE")

# ALLOWED_ORIGINS controla el CORS. En desarrollo, sin configurar, se
# permite cualquier origen para poder probar el widget como archivo HTML
# local. En produccion se debe definir la variable de entorno
# ALLOWED_ORIGINS con el dominio real de la web del instituto, ej:
#   ALLOWED_ORIGINS=https://www.istte.edu.ec
# (varios dominios separados por coma).
#
# ENTORNO=production (ver render.yaml) hace que, si ALLOWED_ORIGINS no esta
# definida, el servidor falle al arrancar en vez de exponer /query a
# cualquier origen por accidente (fail-closed en vez de fail-open).
_allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
_entorno = os.getenv("ENTORNO", "development")

if _allowed_origins_env:
    allowed_origins = [origin.strip() for origin in _allowed_origins_env.split(",")]
elif _entorno == "development":
    allowed_origins = ["*"]
else:
    raise RuntimeError(
        f"ENTORNO={_entorno!r} pero falta ALLOWED_ORIGINS. "
        "En produccion hay que definir los dominios permitidos explicitamente "
        "(ver .env.example) — no se arranca con CORS abierto a cualquier origen."
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
