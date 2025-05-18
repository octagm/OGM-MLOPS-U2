from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)


# Estructura para almacenar las predicciones
class PredictionStore:
    def __init__(self, file_path="predicciones.json"):
        self.file_path = file_path
        self.predictions = self._load_predictions()

    def _load_predictions(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except:
                return {"ENFERMO LEVE": 0, "NO ENFERMO": 0, "ENFERMEDAD AGUDA": 0,
                        "ENFERMEDAD CRÓNICA": 0, "ENFERMEDAD TERMINAL": 0, "OTRO": 0, "historial": []}
        else:
            return {"ENFERMO LEVE": 0, "NO ENFERMO": 0, "ENFERMEDAD AGUDA": 0,
                    "ENFERMEDAD CRÓNICA": 0, "ENFERMEDAD TERMINAL": 0, "OTRO": 0, "historial": []}

    def save_prediction(self, prediction, datos):
        # Incrementar contador de categoría
        if prediction in self.predictions:
            self.predictions[prediction] += 1
        else:
            self.predictions["OTRO"] += 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.predictions["historial"].append({
            "fecha": timestamp,
            "resultado": prediction,
            "datos": datos
        })

        with open(self.file_path, 'w') as f:
            json.dump(self.predictions, f)

    def get_report(self):
        contadores = {k: v for k, v in self.predictions.items() if k != "historial"}
        ultimas_predicciones = self.predictions["historial"][-5:] if len(self.predictions["historial"]) > 0 else []
        ultima_fecha = self.predictions["historial"][-1]["fecha"] if len(
            self.predictions["historial"]) > 0 else "Sin predicciones"

        return {
            "predicciones_por_categoria": contadores,
            "ultimas_predicciones": ultimas_predicciones,
            "ultima_prediccion_fecha": ultima_fecha
        }


# Instancia global del almacén de predicciones
prediction_store = PredictionStore()


def diagnostico(temperatura, ritmo_cardiaco, saturacion_oxigeno):
    if 36 <= temperatura < 37.5 and 60 <= ritmo_cardiaco <= 100 and saturacion_oxigeno >= 95:
        return "NO ENFERMO"
    elif 37.5 <= temperatura < 38.5 and 100 < ritmo_cardiaco <= 120 and 92 <= saturacion_oxigeno < 95:
        return "ENFERMO LEVE"
    elif 38.5 <= temperatura < 40 and ritmo_cardiaco > 120 and 90 <= saturacion_oxigeno < 92:
        return "ENFERMEDAD AGUDA"
    elif temperatura >= 40 and 60 <= ritmo_cardiaco < 100 and 85 <= saturacion_oxigeno < 90:
        return "ENFERMEDAD CRÓNICA"
    elif temperatura >= 40 and ritmo_cardiaco < 60 and saturacion_oxigeno < 85:
        return "ENFERMEDAD TERMINAL"
    else:
        return "Valores fuera de rango, consulte a un médico."


@app.route('/diagnostico', methods=['POST'])
def diagnosticar():
    data = request.json
    temperatura = float(data["temperatura"])
    ritmo_cardiaco = int(data["ritmo_cardiaco"])
    saturacion_oxigeno = int(data["saturacion_oxigeno"])

    resultado = diagnostico(temperatura, ritmo_cardiaco, saturacion_oxigeno)

    # Guardar la predicción
    prediction_store.save_prediction(resultado, {
        "temperatura": temperatura,
        "ritmo_cardiaco": ritmo_cardiaco,
        "saturacion_oxigeno": saturacion_oxigeno
    })

    return jsonify({"resultado": resultado})


@app.route('/reporte', methods=['GET'])
def generar_reporte():
    reporte = prediction_store.get_report()
    return jsonify(reporte)

if __name__ == '__main__':
    import sys
    import time
    app.run(host='0.0.0.0', port=5000)