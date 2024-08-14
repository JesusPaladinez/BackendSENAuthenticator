import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

# Establece la variable de entorno para la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_senauthenticator.settings')

# Configura la aplicación WSGI
application = get_wsgi_application()

if __name__ == "__main__":
    # Ejecuta el servidor Waitress
    print("Starting server on http://localhost:8080/senauthenticator/")
    serve(application, host='0.0.0.0', port=8080)
