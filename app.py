from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

# Simulamos la base de datos en memoria
inventario_herramientas = [
    {"id": 1, "nombre": "Revolvedora de Cemento", "marca": "Cemex", "precio_dia": 500.00, "estado": "disponible"},
    {"id": 2, "nombre": "Bailarina Compactadora", "marca": "Mikasa", "precio_dia": 800.00, "estado": "rentado"},
    {"id": 3, "nombre": "Rompedora de Concreto", "marca": "Bosch", "precio_dia": 1200.00, "estado": "disponible"},
    {"id": 4, "nombre": "Planta de Luz", "marca": "Honda", "precio_dia": 600.00, "estado": "disponible"}
]

# La ruta principal ahora carga la página web (index.html)
@app.route('/')
def home():
    return render_template('index.html', maquinas=inventario_herramientas)

# Mantenemos esta ruta por si el profe quiere ver que la API cruda sigue existiendo
@app.route('/api/maquinas')
def obtener_maquinas():
    return jsonify(inventario_herramientas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)