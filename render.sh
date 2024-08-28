# Actualiza pip y setuptools
pip install --upgrade pip setuptools

# Instala primero las dependencias críticas del sistema
apt-get update && apt-get install -y build-essential cmake

# Instala dlib desde un repositorio para disminuir el consumo de memoria RAM
pip install dlib --find-links https://pypi.anaconda.org/menpo/simple

# Luego instala el resto de las dependencias
pip install -r requirements.txt

# Migraciones y archivos estáticos
python manage.py migrate && python manage.py collectstatic --noinput
