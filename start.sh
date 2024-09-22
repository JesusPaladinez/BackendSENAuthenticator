#!/bin/bash

# Establece el puerto por defecto si no está definido
PORT=${PORT:-8000}

# Recoge los archivos estáticos (si aplica)
/opt/venv/bin/python /Backend/manage.py collectstatic --no-input

# Inicia el servidor Gunicorn con la configuración adecuada
exec /opt/venv/bin/gunicorn proyecto_senauthenticator.wsgi:application --bind 0.0.0.0:$PORT --workers 3
