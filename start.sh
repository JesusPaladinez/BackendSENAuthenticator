#!/bin/bash

# Establece el puerto por defecto si no está definido
PORT=${PORT:-8000}

# Inicia el servidor de Django
exec /opt/venv/bin/python /Backend/manage.py runserver 0.0.0.0:$PORT
