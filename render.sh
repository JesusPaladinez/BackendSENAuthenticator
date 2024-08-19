# Actualiza pip y setuptools a la última versión
pip install --upgrade pip setuptools

# Instala las dependencias desde requirements.txt, migra a la base de datos y carga los estilos
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

