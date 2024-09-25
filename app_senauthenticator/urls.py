from django.urls import path
from app_senauthenticator.controllers import programa, ficha, usuario, objeto, ingreso, tutor, oficina
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
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
