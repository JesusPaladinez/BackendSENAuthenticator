# Usa una imagen base de Python (por ejemplo, Python 3.10)
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Instala Gunicorn explícitamente en caso de que no se haya instalado desde requirements.txt
RUN pip install gunicorn

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Ejecuta los comandos de migración y recolecta archivos estáticos
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expone el puerto en el que Gunicorn se ejecutará
EXPOSE 8000

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "proyecto_senauthenticator.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
