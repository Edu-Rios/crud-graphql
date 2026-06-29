# Usamos una versión ligera de Python
FROM python:3.10-slim

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos la lista de librerías y las instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de tu backend
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para encender el servidor permitiendo conexiones externas
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]