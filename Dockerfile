# Usamos una versión ligera de Python
FROM python:3.9-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero las dependencias y las instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# El comando que arranca la aplicación
CMD ["python", "app.py"]