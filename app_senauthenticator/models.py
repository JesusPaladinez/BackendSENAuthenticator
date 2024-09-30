from djongo import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver 
from django.urls import reverse 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


tipo_documento_usuario=[
    ('Cédula de ciudadanía','Cédula de ciudadanía'),
    ('Tarjeta de identidad','Tarjeta de identidad'),
    ('Cédula de extranjería','Cédula de extranjería'),
]

tipo_documento_tutor=[
    ('Cédula de ciudadanía','Cédula de ciudadanía'),
    ('Cédula de extranjería','Cédula de extranjería'),
]

tipo_rol=[
    ('Aprendiz','Aprendiz'),
    ('Instructor','Instructor'),
    ('Administrador','Administrador'),
    ('Guardia de seguridad','Guardia de seguridad'),
    ('Usuario','Usuario'),
]

jornada_ficha=[
    ('Mañana','Mañana'),
    ('Tarde','Tarde'),
    ('Noche','Noche'),
]

tipo_formacion=[
    ('Tecnólogo','Tecnólogo'),
    ('Técnico','Técnico'),
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
    programa_ficha=models.ForeignKey(Programa, on_delete=models.PROTECT, null=True, db_column='programa_ficha')

    def __str__(self) -> str:
        return self.numero_ficha
    

class Usuario(AbstractUser):
    tipo_documento_usuario=models.CharField(max_length=50, choices=tipo_documento_usuario, default='Cedula de ciudadania', db_column='tipo_documento_usuario')
    numero_documento_usuario=models.CharField(max_length=20, unique=True, db_column='numero_documento_usuario')
    genero_usuario=models.CharField(max_length=9, choices=genero, blank=True, null=True, db_column='genero_usuario')  
    rol_usuario = models.CharField(max_length=20, choices=tipo_rol, blank=True, null=True, db_column='rol_usuario') 
    ficha_usuario=models.ForeignKey(Ficha, on_delete=models.PROTECT, blank=True, null=True, db_column='ficha_usuario')
    face_register = models.URLField(blank=True, null=True, max_length=500, db_column='face_register')

    # nombre_usuario=models.CharField(max_length=50, db_column='nombre_usuario')
    # apellidos_usuario=models.CharField(max_length=50, db_column='apellidos_usuario')
    # correo_usuario=models.CharField(max_length=50, db_column='correo_personal_usuario') 
    # password=models.CharField(max_length=30, db_column='contrasenia_usuario')
    # username=models.CharField(max_length=30, db_column='username')

    USERNAME_FIELD = 'numero_documento_usuario' # se cambia el username por el numero_documento_usuario para poder autenticarse
    REQUIRED_FIELDS = ['username', 'email'] # campos requeridos al momento de crear un super usuario

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_permissions_set',  
        blank=True
    )

    def __str__(self) -> str:
        return self.numero_documento_usuario


class RegistroFacial(models.Model):
    datos_biometricos_registro=models.ImageField(upload_to=f'datos_biometricos_registro', db_column='datos_biometricos_registro')
    fecha_hora_registro=models.DateTimeField(auto_now_add=True, db_column='fecha_hora_registro') 
    usuario_registro_facial=models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, db_column='usuario_registro_facial')


class Oficina(models.Model):
    nombre_oficina=models.CharField(max_length=40, db_column='nombre_oficina')

    def __str__(self) -> str:
        return f'{self.nombre_oficina}'


class UsuarioExterno(AbstractUser):
    tipo_documento_usuario_externo=models.CharField(max_length=50, choices=tipo_documento_usuario, default='Cedula de ciudadania', db_column='tipo_documento_usuario')
    numero_documento_usuario_externo=models.CharField(max_length=20, unique=True, db_column='numero_documento_usuario')
    descripcion_usuario_externo=models.TextField(db_column='descripcion_usuario_externo')
    oficina_usuario_externo = models.ForeignKey(Oficina, on_delete=models.PROTECT, db_column='oficina')
    


    REQUIRED_FIELDS = 'numero_documento_usuario' # se cambia el username por el numero_documento_usuario para poder autenticarse

    groups = models.ManyToManyField(
        Group,
        related_name='usuarioexterno_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarioexterno_permissions_set', 
        blank=True
    )

    def __str__(self) -> str:
        return self.numero_documento_usuario
    


class Ingreso(models.Model):
    datos_biometricos_ingreso=models.ImageField(upload_to=f'datos_biometricos_ingreso', db_column='datos_biometricos_ingreso')    
    fecha_hora_ingreso=models.DateTimeField(auto_now_add=True, db_column='fecha_hora_ingreso')
    usuario_ingreso=models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, db_column='usuario_ingreso')


class Objeto(models.Model):
    marca_objeto = models.CharField(max_length=20, db_column='marca_objeto')
    modelo_objeto = models.CharField(max_length=20, db_column='modelo_objeto')
    descripcion_objeto = models.TextField(db_column='descripcion_objeto')
    foto_objeto = models.URLField(max_length=300,db_column='foto_objeto', blank=True, null=True)  # Guardarás la URL aquí
    usuario_objeto = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_objeto')

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
    usuario_tutor=models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, db_column='usuario_tutor')

    def __str__(self) -> str:
        return f'{self.nombre_tutor} {self.apellido_tutor}'


import uuid
class PasswordReset(models.Model):
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario')
    reset_id=models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when=models.DateTimeField(auto_now_add=True)  # Corregido a DateTimeField
    
    def __str__(self):
        return f"password reset for {self.usuario.username} with name {self.usuario.first_name} at {self.created_when}"
    

@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("password-reset/")+str(token)

    print(token)
    print(full_link)

    context = {
        'full_link': full_link,
        'email_adress': reset_password_token.user.email
    }