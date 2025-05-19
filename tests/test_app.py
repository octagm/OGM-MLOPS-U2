import pytest
import sys
import os
import json

# Agregando el directorio raíz del proyecto al Path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, diagnostico

REPORTE_PATH = "reporte.json"

@pytest.fixture(autouse=True)
def limpiar_reporte():
    # Esta función se ejecuta automáticamente antes de cada test
    if os.path.exists(REPORTE_PATH):
        os.remove(REPORTE_PATH)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_diagnostico_funcion():
    assert diagnostico(36.5, 80, 98) == "NO ENFERMO"
    assert diagnostico(37.8, 110, 93) == "ENFERMO LEVE"
    assert diagnostico(39.0, 130, 91) == "ENFERMEDAD AGUDA"
    assert diagnostico(40.2, 70, 88) == "ENFERMEDAD CRÓNICA"
    assert diagnostico(40.5, 50, 80) == "ENFERMEDAD TERMINAL"

def test_post_diagnostico_and_reporte(client):
    response = client.post('/diagnostico', json={
        "temperatura": 39.0,
        "ritmo_cardiaco": 130,
        "saturacion_oxigeno": 91
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["resultado"] == "ENFERMEDAD AGUDA"

    # Verificar que el reporte refleja la predicción
    response = client.get('/reporte')
    assert response.status_code == 200
    reporte = response.get_json()
    assert "predicciones_por_categoria" in reporte
    assert "ultimas_predicciones" in reporte
    assert "ultima_prediccion_fecha" in reporte
    assert "ENFERMEDAD AGUDA" in reporte["predicciones_por_categoria"]
    assert reporte["predicciones_por_categoria"]["ENFERMEDAD AGUDA"] >= 1

def test_multiples_predicciones(client):
    entradas = [
        {"temperatura": 36.5, "ritmo_cardiaco": 80,  "saturacion_oxigeno": 98, "esperado": "NO ENFERMO"},
        {"temperatura": 37.8, "ritmo_cardiaco": 110, "saturacion_oxigeno": 93, "esperado": "ENFERMO LEVE"},
        {"temperatura": 39.0, "ritmo_cardiaco": 130, "saturacion_oxigeno": 91, "esperado": "ENFERMEDAD AGUDA"},
        {"temperatura": 40.2, "ritmo_cardiaco": 70,  "saturacion_oxigeno": 88, "esperado": "ENFERMEDAD CRÓNICA"},
        {"temperatura": 40.5, "ritmo_cardiaco": 50,  "saturacion_oxigeno": 80, "esperado": "ENFERMEDAD TERMINAL"},
        {"temperatura": 40.5, "ritmo_cardiaco": 50,  "saturacion_oxigeno": 80, "esperado": "ENFERMEDAD TERMINAL"}  # Repetida
    ]

    conteo_esperado = {}

    # Enviar cada predicción
    for entrada in entradas:
        response = client.post('/diagnostico', json={
            "temperatura": entrada["temperatura"],
            "ritmo_cardiaco": entrada["ritmo_cardiaco"],
            "saturacion_oxigeno": entrada["saturacion_oxigeno"]
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["resultado"] == entrada["esperado"]

        # Actualizar conteo esperado
        conteo_esperado[entrada["esperado"]] = conteo_esperado.get(entrada["esperado"], 0) + 1

    # Obtener el reporte final
    response = client.get('/reporte')
    assert response.status_code == 200
    reporte = response.get_json()
    predicciones_por_categoria = reporte["predicciones_por_categoria"]

    # Validar que el reporte tenga las cantidades correctas
    for categoria, cantidad in conteo_esperado.items():
        assert predicciones_por_categoria.get(categoria, 0) == cantidad
