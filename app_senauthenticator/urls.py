from django.urls import path
from app_senauthenticator.controllers import programa, ficha, usuario, objeto, ingreso, tutor, oficina
from app_senauthenticator.controllers.registro_facial import RegistroFacial
from app_senauthenticator.controllers.inicio_sesion_facial import InicioSesionFacial
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Oficina
    path('oficina/<int:pk>/', oficina.oficina_controlador, name="cont_oficina"),
    path('oficina/', oficina.oficina_controlador, name="cont_oficina"),
    # Programa
    path('programa/', programa.programa_controlador, name="cont_programa"),
    path('programa/<int:pk>/', programa.programa_controlador, name="cont_programa"),
    # Ficha
    path('ficha/', ficha.ficha_controlador, name="cont_ficha"),
    path('ficha/<int:pk>/', ficha.ficha_controlador, name="cont_ficha"),
    # Usuario
    path('usuario/', usuario.usuario_controlador, name="cont_usuario"),
    path('usuario/<int:pk>/', usuario.usuario_controlador, name="cont_usuario_detail"), 
    path('inicioSesion/', usuario.inicio_sesion, name="inicio_sesion"),
    path('validarToken/', usuario.validarToken, name='protected_view'),
    # Objeto
    path('objeto/', objeto.objeto_controlador, name="cont_objeto"),
    path('objeto/<int:pk>/', objeto.objeto_controlador, name="cont_objeto"),
    # Tutor
    path('tutor/', tutor.tutor_controlador),
    path('tutor/<int:pk>/', tutor.tutor_controlador),
    # Ingreso
    path('ingreso/', ingreso.ingreso_controlador, name="cont_ingreso"),
    path('ingreso/<int:pk>/', ingreso.ingreso_controlador, name="cont_ingreso"),
    # Registro Facial
    path('inicioSesionFacial/', InicioSesionFacial.as_view()),
    path('registroFacial/', RegistroFacial.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
