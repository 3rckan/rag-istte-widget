# qa/test_widget.py
# QA automatizado de la burbuja flotante con Playwright.
#
# No depende de Ollama/ChromaDB: el endpoint /query se intercepta con
# page.route() para devolver una respuesta fija, asi que estas pruebas
# validan la INTERFAZ (burbuja, panel, mensajes) y no el modelo. La
# evaluacion del modelo en si ya la cubre scripts/evaluate.py (Sprint 4).
#
# Requiere el backend corriendo en http://127.0.0.1:8000:
#   uvicorn app.main:app --reload
# y luego, en otra terminal:
#   pytest qa/ -v

import pathlib

import pytest
from playwright.sync_api import Page, expect

HOST_PRUEBA = (pathlib.Path(__file__).parent / "host_prueba.html").resolve().as_uri()
RESPUESTA_FALSA = {
    "respuesta": "Las matriculas se abren en el periodo academico indicado en el calendario.",
    "fuentes": [{"archivo": "reglamento_ejemplo.pdf"}],
}


def _mockear_query(page: Page):
    """Reemplaza el backend real del /query por una respuesta fija y rapida."""
    page.route("**/query", lambda route: route.fulfill(json=RESPUESTA_FALSA))


def test_burbuja_visible_en_pagina_host(page: Page):
    page.goto(HOST_PRUEBA)
    burbuja = page.locator("#istte-chat-burbuja")
    expect(burbuja).to_be_visible()


def test_panel_cerrado_al_inicio(page: Page):
    page.goto(HOST_PRUEBA)
    panel = page.locator("#istte-chat-panel")
    expect(panel).not_to_have_class("abierto")


def test_click_burbuja_abre_panel(page: Page):
    page.goto(HOST_PRUEBA)
    page.locator("#istte-chat-burbuja").click()
    panel = page.locator("#istte-chat-panel")
    expect(panel).to_have_class("abierto")

    iframe = page.frame_locator("#istte-chat-panel iframe")
    expect(iframe.locator("#chat-header")).to_be_visible()


def test_boton_cerrar_dentro_del_iframe_cierra_panel(page: Page):
    page.goto(HOST_PRUEBA)
    page.locator("#istte-chat-burbuja").click()
    panel = page.locator("#istte-chat-panel")
    expect(panel).to_have_class("abierto")

    iframe = page.frame_locator("#istte-chat-panel iframe")
    iframe.locator("#chat-close").click()

    expect(panel).not_to_have_class("abierto")


def test_enviar_pregunta_muestra_respuesta_y_fuente(page: Page):
    page.goto(HOST_PRUEBA)
    _mockear_query(page)

    page.locator("#istte-chat-burbuja").click()
    iframe = page.frame_locator("#istte-chat-panel iframe")

    iframe.locator("#chat-input").fill("Cuando son las matriculas?")
    iframe.locator("#chat-form button[type=submit]").click()

    expect(iframe.locator(".msg.user").last).to_have_text("Cuando son las matriculas?")
    expect(iframe.locator(".msg.bot").last).to_contain_text(RESPUESTA_FALSA["respuesta"])
    expect(iframe.locator(".fuentes").last).to_contain_text("reglamento_ejemplo.pdf")


def test_error_de_backend_muestra_mensaje_de_error(page: Page):
    page.goto(HOST_PRUEBA)
    page.route("**/query", lambda route: route.abort())

    page.locator("#istte-chat-burbuja").click()
    iframe = page.frame_locator("#istte-chat-panel iframe")

    iframe.locator("#chat-input").fill("Pregunta cualquiera")
    iframe.locator("#chat-form button[type=submit]").click()

    expect(iframe.locator(".msg.bot").last).to_contain_text("Error al conectar")


@pytest.mark.parametrize("ancho,alto", [(375, 667), (390, 844)])
def test_panel_responsivo_en_moviles(page: Page, ancho, alto):
    page.set_viewport_size({"width": ancho, "height": alto})
    page.goto(HOST_PRUEBA)
    page.locator("#istte-chat-burbuja").click()
    panel = page.locator("#istte-chat-panel")
    box = panel.bounding_box()
    assert box is not None
    assert box["width"] <= ancho
