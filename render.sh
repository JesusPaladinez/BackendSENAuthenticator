# Actualiza pip y setuptools a la última versión
pip install --upgrade pip setuptools

# Instala las dependencias del sistema necesarias para compilar dlib y otras librerías
apt-get update && apt-get install -y build-essential cmake

# Instala las dependencias desde requirements.txt, migra la base de datos y carga los estilos
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
