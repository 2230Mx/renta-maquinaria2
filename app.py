from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
import os
import time

app = Flask(__name__)

def obtener_conexion():
    # Intentamos conectar hasta 5 veces, esperando 3 segundos entre cada intento
    retries = 5
    while retries > 0:
        try:
            conexion = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'db'),
                user=os.environ.get('DB_USER', 'admin'),
                password=os.environ.get('DB_PASSWORD', 'adminpassword'),
                database=os.environ.get('DB_NAME', 'maquinaria_db')
            )
            return conexion
        except Error as e:
            print(f"Esperando a MySQL... Te quedan {retries-1} intentos.")
            retries -= 1
            time.sleep(3)
    return None

def init_db():
    conexion = obtener_conexion()
    if conexion and conexion.is_connected():
        cursor = conexion.cursor()
        
        # 1. Creamos la tabla del inventario si no existe
        tabla_maquinas = """
        CREATE TABLE IF NOT EXISTS maquinas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            marca VARCHAR(50),
            precio_dia DECIMAL(10, 2) NOT NULL,
            estado VARCHAR(20) DEFAULT 'disponible'
        )
        """
        cursor.execute(tabla_maquinas)
        
        # 2. Insertamos una máquina de prueba solo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM maquinas")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO maquinas (nombre, marca, precio_dia) 
                VALUES ('Revolvedora de Cemento', 'Cemex', 500.00)
            """)
            conexion.commit()

        cursor.close()
        conexion.close()
        print("¡Base de datos lista y con tablas creadas!")

# Ejecutamos la función justo antes de que arranque el servidor Flask
init_db()

@app.route('/')
def home():
    return jsonify({"status": "online", "mensaje": "API conectada a MySQL exitosamente"})

# Nuevo endpoint para ver tu inventario
@app.route('/api/maquinas')
def obtener_maquinas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maquinas")
    maquinas = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return jsonify(maquinas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)