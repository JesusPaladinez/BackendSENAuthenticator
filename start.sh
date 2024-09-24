#!/bin/bash

# Imprime el puerto para verificar que está configurado correctamente
echo "Starting application on port: $PORT"

# Establece el puerto por defecto si no está definido
PORT=${PORT:-8080}

# Aplica las migraciones
/opt/venv/bin/python /Backend/manage.py migrate --no-input

# Recoge los archivos estáticos
/opt/venv/bin/python /Backend/manage.py collectstatic --no-input

# Inicia el servidor Gunicorn con configuración de tiempo de espera ajustada
exec /opt/venv/bin/gunicorn proyecto_senauthenticator.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
