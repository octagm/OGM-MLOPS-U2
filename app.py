from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- Importa CORS

app = Flask(__name__)
CORS(app)  # <--- Habilita CORS en toda la app

def diagnostico(temperatura, ritmo_cardiaco, saturacion_oxigeno):
    if 36 <= temperatura < 37.5 and 60 <= ritmo_cardiaco <= 100 and saturacion_oxigeno >= 95:
        return "NO ENFERMO"
    elif 37.5 <= temperatura < 38.5 and 100 < ritmo_cardiaco <= 120 and saturacion_oxigeno >= 92:
        return "ENFERMO LEVE"
    elif temperatura >= 38.5 and ritmo_cardiaco > 120 and saturacion_oxigeno < 92:
        return "ENFERMEDAD AGUDA"
    elif 37 <= temperatura < 38 and 60 <= ritmo_cardiaco < 100 and saturacion_oxigeno < 90:
        return "ENFERMEDAD CRÓNICA"
    else:
        return "Valores fuera de rango, consulte a un médico."

@app.route('/diagnostico', methods=['POST'])
def diagnosticar():
    data = request.json
    resultado = diagnostico(
        float(data["temperatura"]),
        int(data["ritmo_cardiaco"]),
        int(data["saturacion_oxigeno"])
    )
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
