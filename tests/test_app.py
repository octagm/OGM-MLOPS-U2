import pytest
from app import app, diagnostico

# Cliente de pruebas de Flask
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

def test_post_diagnostico(client):
    response = client.post('/diagnostico', json={
        "temperatura": 37.8,
        "ritmo_cardiaco": 110,
        "saturacion_oxigeno": 93
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["resultado"] == "ENFERMO LEVE"

def test_get_reporte(client):
    response = client.get('/reporte')
    assert response.status_code == 200
    data = response.get_json()
    assert "predicciones_por_categoria" in data
    assert "ultimas_predicciones" in data
    assert "ultima_prediccion_fecha" in data
