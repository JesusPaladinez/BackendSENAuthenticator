from djongo import models
from django.contrib.auth.models import AbstractUser


tipo_documento_usuario=[
    ('Cedula de ciudadania','Cedula de ciudadania'),
    ('Tarjeta de Identidad','Tarjeta de Identidad'),
    ('Cedula de extranjeria','Cedula de extranjeria'),
]

tipo_documento_tutor=[
    ('Cedula de ciudadania','Cedula de ciudadania'),
    ('Cedula de extranjeria','Cedula de extranjeria'),
]

tipo_rol=[
    ('Aprendiz','Aprendiz'),
    ('Instructor','Instructor'),
    ('Administrador','Administrador'),
    ('Funcionario','Funcionario'),
    ('Guardia de seguridad','Guardia de seguridad'),
    ('Usuario','Usuario'),
]

jornada_ficha=[
    ('Mañana','Mañana'),
    ('Tarde','Tarde'),
    ('Noche','Noche'),
]

tipo_formacion=[
    ('Tecnologo','Tecnologo'),
    ('Tecnico','Tecnico'),
]

genero = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
] 
    

class Programa(models.Model):
    nombre_programa=models.CharField(max_length=100, db_column='nombre_programa')
    tipo_formacion_programa=models.CharField(max_length=30,choices=tipo_formacion, db_column='tipo_formacion_programa')

    def __str__(self) -> str:
        return self.nombre_programa
    

class Ficha(models.Model):
    numero_ficha=models.CharField(max_length=20, unique=True, db_column='numero_ficha')
    aprendices_matriculados_ficha=models.IntegerField(db_column='aprendices_matriculados_ficha')
    aprendices_actuales_ficha=models.IntegerField(db_column='aprendices_actuales_ficha')
    jornada_ficha=models.CharField(max_length=50, choices=jornada_ficha, db_column='jornada_ficha')
    programa_ficha=models.ForeignKey(Programa, on_delete=models.PROTECT, default=1, db_column='programa_ficha')

    def __str__(self) -> str:
        return self.numero_ficha
    

class Usuario(AbstractUser):
    tipo_documento_usuario=models.CharField(max_length=50, choices=tipo_documento_usuario, default='Cedula de ciudadania', db_column='tipo_documento_usuario')
    numero_documento_usuario=models.CharField(max_length=20, unique=True, db_column='numero_documento_usuario')
    genero_usuario=models.CharField(max_length=9, choices=genero, db_column='genero_usuario')  
    rol_usuario = models.CharField(max_length=20, choices=tipo_rol, default='Usuario', db_column='rol_usuario') 
    ficha_usuario=models.ForeignKey(Ficha, on_delete=models.PROTECT, default=1, db_column='ficha_usuario')
    # nombre_usuario=models.CharField(max_length=50, db_column='nombre_usuario')
    # apellidos_usuario=models.CharField(max_length=50, db_column='apellidos_usuario')
    # correo_usuario=models.CharField(max_length=50, db_column='correo_personal_usuario') 
    # password=models.CharField(max_length=30, db_column='contrasenia_usuario')
    # username=models.CharField(max_length=30, db_column='username')

    USERNAME_FIELD = 'numero_documento_usuario' # se cambia el username por el numero_documento_usuario para poder autenticarse
    REQUIRED_FIELDS = ['username', 'email'] # campos requeridos al momento de crear un super usuario

    def __str__(self) -> str:
        return self.numero_documento_usuario


class RegistroFacial(models.Model):
    datos_biometricos_registro=models.ImageField(upload_to=f'datos_biometricos_registro', db_column='datos_biometricos_registro')
    fecha_hora_registro=models.DateTimeField(auto_now_add=True, db_column='fecha_hora_registro') 
    usuario_registro_facial=models.ForeignKey(Usuario, on_delete=models.PROTECT, default=1, db_column='usuario_registro_facial')


class Ingreso(models.Model):
    datos_biometricos_ingreso=models.ImageField(upload_to=f'datos_biometricos_ingreso', db_column='datos_biometricos_ingreso')    
    fecha_hora_ingreso=models.DateTimeField(auto_now_add=True, db_column='fecha_hora_ingreso')
    usuario_ingreso=models.ForeignKey(Usuario, on_delete=models.PROTECT, default=1, db_column='usuario_ingreso')


class Objeto(models.Model):
    marca_objeto=models.CharField(max_length=20, db_column='marca_objeto')
    modelo_objeto=models.CharField(max_length=20, db_column='modelo_objeto')
    descripcion_objeto=models.TextField(max_length=1000, db_column='descripcion_objeto')
    foto_objeto=models.ImageField(upload_to=f"foto_objeto", db_column='foto_objeto')
    usuario_objeto=models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_objeto')

    def __str__(self) -> str:
        return f'{self.marca_objeto} {self.modelo_objeto}'


class Tutor(models.Model):
    nombre_tutor=models.CharField(max_length=50, db_column='nombre_tutor')
    apellido_tutor=models.CharField(max_length=50, db_column='apellido_tutor')
    tipo_documento_tutor=models.CharField(max_length=50, choices=tipo_documento_tutor, default='Cedula de ciudadania', db_column='tipo_documento_tutor')
    numero_documento_tutor=models.CharField(max_length=20, unique=True, db_column='numero_documento_tutor')
    celular_tutor=models.CharField(max_length=12, db_column='celular_tutor')
    genero_tutor=models.CharField(max_length=20, choices=genero, db_column='genero_tutor')  
    parentezco_tutor=models.CharField(max_length=30, db_column='parentezco_tutor')
    usuario_tutor=models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_tutor')

    def __str__(self) -> str:
        return f'{self.nombre_tutor} {self.apellido_tutor}'
