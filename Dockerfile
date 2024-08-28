FROM continuumio/miniconda3

# Crear un ambiente de conda para el proyecto
RUN conda create -n myenv python=3.10 dlib -c conda-forge

# Activar el ambiente
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copiar archivos del proyecto
WORKDIR /app
COPY . /app

# Instalar otras dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar comandos de migración y recolectar archivos estáticos
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "proyecto_senauthenticator.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
