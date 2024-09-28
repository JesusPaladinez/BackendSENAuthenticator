# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer un directorio de trabajo
WORKDIR /Backend

# Instalar las dependencias del sistema necesarias para compilar dlib, OpenCV y psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpq-dev \
    gcc \
    python3-dev

# Crear un entorno virtual
RUN python -m venv /opt/venv

# Activar el entorno virtual y asegurar que pip esté actualizado
RUN . /opt/venv/bin/activate && pip install --upgrade pip

# Copiar los archivos del proyecto
COPY . /Backend/.

# Instalar las dependencias de Python desde el archivo requirements.txt
RUN . /opt/venv/bin/activate && pip install -r /Backend/requirements.txt

# Recopilar archivos estáticos
RUN . /opt/venv/bin/activate && python /Backend/manage.py collectstatic --noinput

# Copiar el script de inicio y darle permisos de ejecución
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Comando para iniciar la aplicación utilizando el script de inicio
CMD ["/start.sh"]