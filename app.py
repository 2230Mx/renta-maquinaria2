from flask import Flask, jsonify
import os

app = Flask(__name__)

# Simulamos la base de datos en memoria para que no falle en Cloud Run
inventario_herramientas = [
    {"id": 1, "nombre": "Revolvedora de Cemento", "marca": "Cemex", "precio_dia": 500.00, "estado": "disponible"},
    {"id": 2, "nombre": "Bailarina Compactadora", "marca": "Mikasa", "precio_dia": 800.00, "estado": "rentado"},
    {"id": 3, "nombre": "Rompedora de Concreto", "marca": "Bosch", "precio_dia": 1200.00, "estado": "disponible"}
]

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "proyecto": "API Renta de Herramientas de Construcción",
        "mensaje": "¡Contenedor de Python funcionando perfectamente en Google Cloud Run!"
    })

@app.route('/api/maquinas')
def obtener_maquinas():
    return jsonify(inventario_herramientas)

if __name__ == '__main__':
    # Cloud Run inyecta el puerto dinámicamente, por defecto usa el 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)