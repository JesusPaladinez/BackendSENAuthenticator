# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer un directorio de trabajo
WORKDIR /Backend

# Instalar las dependencias del sistema necesarias para compilar dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev

# Crear un entorno virtual
RUN python -m venv /opt/venv

# Activar el entorno virtual y asegurar que pip esté actualizado
RUN . /opt/venv/bin/activate && pip install --upgrade pip

# Copiar los archivos del proyecto
COPY . /Backend/.

# Instalar las dependencias de Python desde el archivo requirements.txt
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Comando para iniciar la aplicación utilizando la variable PORT de Railway
CMD ["/opt/venv/bin/python", "manage.py", "runserver", "0.0.0.0:${PORT}"]
