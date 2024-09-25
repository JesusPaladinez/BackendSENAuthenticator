from django.urls import path
from app_senauthenticator.controllers import programa, ficha, usuario, registro_facial, objeto, ingreso, tutor,recuperar_contraseña,oficina
# from app_senauthenticator.controllers.autenticacion_facial import AutenticacionFacial
from app_senauthenticator.controllers.registro_facial import RegistroFacial
from app_senauthenticator.controllers.inicio_sesion_facial import InicioSesionFacial
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Oficina
    path('oficinas/', oficina.oficina_controlador, name="cont_oficina"),
    path('oficinas/<int:pk>/', oficina.oficina_controlador, name="cont_oficina"),
    # Programa
    path('programas/', programa.programa_controlador, name="cont_programa"),
    path('programas/<int:pk>/', programa.programa_controlador, name="cont_programa"),
    # Ficha
    path('fichas/', ficha.ficha_controlador, name="cont_ficha"),
    path('fichas/<int:pk>/', ficha.ficha_controlador, name="cont_ficha"),
    # Usuario
    path('usuarios/', usuario.usuario_controlador, name="cont_usuario"),
    path('usuarios/<int:pk>/', usuario.usuario_controlador, name="cont_usuario_detail"), 
    path('inicio-sesion/', usuario.inicio_sesion, name="inicio_sesion"),
    path('validar-token/', usuario.validarToken, name='protected_view'),
    # Objeto
    path('objetos/', objeto.objeto_controlador, name="cont_objeto"),
    path('objetos/<int:pk>/', objeto.objeto_controlador, name="cont_objeto"),
    # Tutor
    path('tutores/', tutor.tutor_controlador),
    path('tutores/<int:pk>/', tutor.tutor_controlador),
    # Ingreso
    path('ingresos/', ingreso.ingreso_controlador, name="cont_ingreso"),
    path('ingresos/<int:pk>/', ingreso.ingreso_controlador, name="cont_ingreso"),
    # Registro Facial
    path('inicio-sesion-facial/', InicioSesionFacial.as_view()),
    path('registro-facial/', RegistroFacial.as_view()),
    path('tutor/', tutor.tutor_controlador),
    path('tutor/<int:pk>/', tutor.tutor_controlador),
    path('ingreso/', ingreso.ingreso_controlador),
    path('ingreso/<int:pk>/', ingreso.ingreso_controlador),
    path('inicioSesion/', usuario.inicio_sesion),
    path('perfil/', usuario.perfil),
    # recuperar contraseña
    path('forgotpassword/', usuario.ForgotPassword, name='forgot-password'),
    path('passwordresetsent/<str:reset_id>/', usuario.PasswordResetSent, name='password-reset-sent'),
    path('resetpassword/<str:reset_id>/', usuario.ResetPassword, name='reset-password'),
    # path('autenticacionFacial/', AutenticacionFacial.as_view())
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
