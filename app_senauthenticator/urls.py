from django.urls import path
from app_senauthenticator.controllers import programa, ficha, usuario, objeto, ingreso, tutor, oficina, usuario_externo, recuperar_contraseña
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
    path('usuarios/', usuario.usuarios_controlador, name="cont_usuario"),
    path('usuarios/<int:pk>/', usuario.usuario_detalle_controlador, name="cont_usuario_detail"), 
    path('inicio-sesion/', usuario.inicio_sesion, name="inicio_sesion"),
    path('validar-token/', usuario.validarToken, name='protected_view'),
    # Usuario Externo
    path('usuarios-externos/', usuario_externo.usuario_externo_controlador, name="cont_usuario_externo"),
    path('usuarios-externos/<int:pk>/', usuario_externo.usuario_externo_controlador, name="cont_usuario_externo"), 
    # Objeto
    path('objetos/', objeto.objeto_controlador, name="cont_objeto"),
    path('objetos/<int:pk>/', objeto.objeto_controlador, name="cont_objeto"),
    # Tutor
    path('tutores/', tutor.tutor_controlador),
    path('tutores/<int:pk>/', tutor.tutor_controlador),
    # Ingreso
    path('ingresos/', ingreso.ingreso_controlador, name="cont_ingreso"),
    path('ingresos/<int:pk>/', ingreso.ingreso_controlador, name="cont_ingreso"),
    # Reconocimiento Facial
    path('inicio-sesion-facial/', InicioSesionFacial.as_view()),
    path('registro-facial/', RegistroFacial.as_view()),
    path('tutor/', tutor.tutor_controlador),
    path('tutor/<int:pk>/', tutor.tutor_controlador),
    path('ingreso/', ingreso.ingreso_controlador),
    path('ingreso/<int:pk>/', ingreso.ingreso_controlador),
    path('inicioSesion/', usuario.inicio_sesion),

    # recuperar contraseña
    path('forgotpassword/', recuperar_contraseña.ForgotPassword, name='forgot-password'),
    path('passwordresetsent/<str:reset_id>/', recuperar_contraseña.PasswordResetSent, name='password-reset-sent'),
    path('resetpassword/<str:reset_id>/', recuperar_contraseña.ResetPassword, name='reset-password'),
    # path('autenticacionFacial/', AutenticacionFacial.as_view())
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
